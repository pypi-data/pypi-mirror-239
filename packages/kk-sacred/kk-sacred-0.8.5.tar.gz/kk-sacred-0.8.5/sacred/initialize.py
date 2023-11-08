#!/usr/bin/env python
# coding=utf-8

import os
import sys
from collections import OrderedDict, defaultdict
from copy import copy, deepcopy
from importlib import import_module

from sacred.config import (
    ConfigDict,
    chain_evaluate_config_scopes,
    dogmatize,
    load_config_file,
    undogmatize,
)
from sacred.config.config_summary import ConfigSummary
from sacred.config.custom_containers import make_read_only
from sacred.config_helpers import DynamicIngredient
from sacred.host_info import get_host_info
from sacred.randomness import create_rnd, get_seed
from sacred.run import Run
from sacred.utils import (
    convert_to_nested_dict,
    create_basic_stream_logger,
    get_by_dotted_path,
    is_prefix,
    rel_path,
    iterate_flattened,
    set_by_dotted_path,
    recursive_update,
    iter_prefixes,
    join_paths,
    NamedConfigNotFoundError,
    ConfigAddedError,
)
from sacred.settings import SETTINGS


class Scaffold:
    def __init__(
        self,
        config_scopes,
        subrunners,
        path,
        captured_functions,
        commands,
        named_configs,
        config_hooks,
        generate_seed,
    ):
        self.config_scopes = config_scopes
        self.named_configs = named_configs
        self.subrunners = subrunners
        self.path = path
        self.generate_seed = generate_seed
        self.config_hooks = config_hooks
        self.config_updates = {}
        self.config_overrides = {}
        self.named_configs_to_use = []
        self.config = {}
        self.fallback = None
        self.presets = {}
        self.fixture = None  # TODO: rename
        self.logger = None
        self.seed = None
        self.rnd = None
        self._captured_functions = captured_functions
        self.commands = commands
        self.config_mods = None
        self.summaries = []
        self.captured_args = {
            join_paths(cf.prefix, n)
            for cf in self._captured_functions
            for n in cf.signature.arguments
        }
        self.captured_args.add("__doc__")  # allow setting the config docstring

    def set_up_seed(self, rnd=None):
        if self.seed is not None:
            return

        self.seed = self.config.get("seed")
        if self.seed is None:
            self.seed = get_seed(rnd)

        self.rnd = create_rnd(self.seed)

        if self.generate_seed:
            self.config["seed"] = self.seed

        if "seed" in self.config and "seed" in self.config_mods.added:
            self.config_mods.modified.add("seed")
            self.config_mods.added -= {"seed"}

        # Hierarchically set the seed of proper subrunners
        for subrunner_path, subrunner in reversed(list(self.subrunners.items())):
            if is_prefix(self.path, subrunner_path):
                subrunner.set_up_seed(self.rnd)

    def gather_fallbacks(self):
        fallback = {"_log": self.logger}
        for sr_path, subrunner in self.subrunners.items():
            if self.path and is_prefix(self.path, sr_path):
                path = sr_path[len(self.path) :].strip(".")
                set_by_dotted_path(fallback, path, subrunner.config)
            else:
                set_by_dotted_path(fallback, sr_path, subrunner.config)

        # dogmatize to make the subrunner configurations read-only
        self.fallback = dogmatize(fallback)
        self.fallback.revelation()

    def run_named_config(self, config_name):
        if os.path.isfile(config_name):
            nc = ConfigDict(load_config_file(config_name))
        else:
            if config_name not in self.named_configs:
                raise NamedConfigNotFoundError(
                    named_config=config_name,
                    available_named_configs=tuple(self.named_configs.keys()),
                )
            nc = self.named_configs[config_name]

        cfg = nc(
            fixed=self.get_config_updates_recursive(),
            preset=self.presets,
            fallback=self.fallback,
        )

        return undogmatize(cfg)

    def set_up_config(self):
        self.config, self.summaries = chain_evaluate_config_scopes(
            self.config_scopes,
            fixed=self.config_updates,
            preset=self.config,
            fallback=self.fallback,
        )

        self.get_config_modifications()

    def run_config_hooks(self, config, command_name, logger):
        final_cfg_updates = {}
        for ch in self.config_hooks:
            cfg_upup = ch(deepcopy(config), command_name, logger)
            if cfg_upup:
                recursive_update(final_cfg_updates, cfg_upup)
        recursive_update(final_cfg_updates, self.config_updates)
        return final_cfg_updates

    def get_config_modifications(self):
        self.config_mods = ConfigSummary(
            added={key for key, value in iterate_flattened(self.config_updates)},
            overridden={key for key, value in iterate_flattened(self.config_overrides)},
        )
        for cfg_summary in self.summaries:
            self.config_mods.update_from(cfg_summary)

    def get_config_updates_recursive(self):
        config_updates = self.config_updates.copy()
        for sr_path, subrunner in self.subrunners.items():
            if not is_prefix(self.path, sr_path):
                continue
            update = subrunner.get_config_updates_recursive()
            if update:
                config_updates[rel_path(self.path, sr_path)] = update
        return config_updates

    def get_fixture(self):
        if self.fixture is not None:
            return self.fixture

        def get_fixture_recursive(runner):
            for sr_path, subrunner in runner.subrunners.items():
                # I am not sure if it is necessary to trigger all
                subrunner.get_fixture()
                get_fixture_recursive(subrunner)
                sub_fix = copy(subrunner.config)
                sub_path = sr_path
                if is_prefix(self.path, sub_path):
                    sub_path = sr_path[len(self.path) :].strip(".")
                # Note: This might fail if we allow non-dict fixtures
                set_by_dotted_path(self.fixture, sub_path, sub_fix)

        self.fixture = copy(self.config)
        get_fixture_recursive(self)

        return self.fixture

    def finalize_initialization(self, run):
        # look at seed again, because it might have changed during the
        # configuration process
        if "seed" in self.config:
            self.seed = self.config["seed"]
        self.rnd = create_rnd(self.seed)

        for cfunc in self._captured_functions:
            # Setup the captured function
            cfunc.logger = self.logger.getChild(cfunc.__name__)
            seed = get_seed(self.rnd)
            cfunc.rnd = create_rnd(seed)
            cfunc.run = run
            cfunc.config = get_by_dotted_path(
                self.get_fixture(), cfunc.prefix, default={}
            )

            # Make configuration read only if enabled in settings
            if SETTINGS.CONFIG.READ_ONLY_CONFIG:
                cfunc.config = make_read_only(cfunc.config)

        if not run.force:
            self._warn_about_suspicious_changes()

    def _warn_about_suspicious_changes(self):
        for add in sorted(self.config_mods.added):
            if not set(iter_prefixes(add)).intersection(self.captured_args):
                if self.path:
                    add = join_paths(self.path, add)
                self.logger.warning('Added new config entry: "%s"' % add)
                # raise ConfigAddedError(add, config=self.config)
            else:
                self.logger.warning('Added new config entry: "%s"' % add)

        for key, (type_old, type_new) in self.config_mods.typechanged.items():
            if type_old in (int, float) and type_new in (int, float):
                continue
            self.logger.warning(
                'Changed type of config entry "%s" from %s to %s'
                % (key, type_old.__name__, type_new.__name__)
            )

        for cfg_summary in self.summaries:
            for key in cfg_summary.ignored_fallbacks:
                self.logger.warning(
                    'Ignored attempt to set value of "%s", because it is an '
                    "ingredient." % key
                )

    def __repr__(self):
        return "<Scaffold: '{}'>".format(self.path)


def get_configuration(scaffolding):
    config = {}
    for sc_path, scaffold in reversed(list(scaffolding.items())):
        if not scaffold.config:
            continue
        if sc_path:
            set_by_dotted_path(config, sc_path, scaffold.config)
        else:
            config.update(scaffold.config)
    return config


def distribute_named_configs(scaffolding, named_configs):
    for ncfg in named_configs:
        if os.path.exists(ncfg):
            scaffolding[""].use_named_config(ncfg)
        else:
            path, _, cfg_name = ncfg.rpartition(".")
            if path not in scaffolding:
                raise KeyError(
                    'Ingredient for named config "{}" not found'.format(ncfg)
                )
            scaffolding[path].use_named_config(cfg_name)


def initialize_logging(experiment, scaffolding, log_level=None):
    if experiment.logger is None:
        root_logger = create_basic_stream_logger()
    else:
        root_logger = experiment.logger

    for sc_path, scaffold in scaffolding.items():
        if sc_path:
            scaffold.logger = root_logger.getChild(sc_path)
        else:
            scaffold.logger = root_logger

    # set log level
    if log_level is not None:
        try:
            lvl = int(log_level)
        except ValueError:
            lvl = log_level
        root_logger.setLevel(lvl)

    return root_logger, root_logger.getChild(experiment.path)


def create_scaffolding(experiment, sorted_ingredients):
    scaffolding = OrderedDict()
    for ingredient in sorted_ingredients[:-1]:
        scaffolding[ingredient] = Scaffold(
            config_scopes=ingredient.configurations,
            subrunners=OrderedDict(
                [(scaffolding[m].path, scaffolding[m]) for m in ingredient.ingredients]
            ),
            path=ingredient.path,
            captured_functions=ingredient.captured_functions,
            commands=ingredient.commands,
            named_configs=ingredient.named_configs,
            config_hooks=ingredient.config_hooks,
            generate_seed=False,
        )

    scaffolding[experiment] = Scaffold(
        experiment.configurations,
        subrunners=OrderedDict(
            [(scaffolding[m].path, scaffolding[m]) for m in experiment.ingredients]
        ),
        path="",
        captured_functions=experiment.captured_functions,
        commands=experiment.commands,
        named_configs=experiment.named_configs,
        config_hooks=experiment.config_hooks,
        generate_seed=True,
    )

    scaffolding_ret = OrderedDict([(sc.path, sc) for sc in scaffolding.values()])
    if len(scaffolding_ret) != len(scaffolding):
        raise ValueError(
            "The pathes of the ingredients are not unique. "
            "{}".format([s.path for s in scaffolding])
        )

    return scaffolding_ret


def gather_ingredients_topological(ingredient):
    sub_ingredients = defaultdict(int)
    for sub_ing, depth in ingredient.traverse_ingredients():
        sub_ingredients[sub_ing] = max(sub_ingredients[sub_ing], depth)
    return sorted(sub_ingredients, key=lambda x: -sub_ingredients[x])


def get_config_modifications(scaffolding):
    config_modifications = ConfigSummary()
    for sc_path, scaffold in scaffolding.items():
        config_modifications.update_add(scaffold.config_mods, path=sc_path)
    return config_modifications


def get_command(scaffolding, command_path):
    path, _, command_name = command_path.rpartition(".")
    if path not in scaffolding:
        raise KeyError('Ingredient for command "%s" not found.' % command_path)

    if command_name in scaffolding[path].commands:
        return scaffolding[path].commands[command_name]
    else:
        if path:
            raise KeyError(
                'Command "%s" not found in ingredient "%s" possible commands: [%s]' % (command_name, path,
                                                                                       ",".join(scaffolding[path].commands.keys()))
            )
        else:
            raise KeyError('Command "%s" not found' % command_name)


def find_best_match(path, prefixes):
    """Find the Ingredient that shares the longest prefix with path."""
    path_parts = path.split(".")
    for p in prefixes:
        if len(p) <= len(path_parts) and p == path_parts[: len(p)]:
            return ".".join(p), ".".join(path_parts[len(p) :])
    return "", path


def distribute_presets(sc_path, prefixes, scaffolding, config_updates):
    for path, value in iterate_flattened(config_updates):
        if sc_path:
            path = sc_path + "." + path
        scaffold_name, suffix = find_best_match(path, prefixes)
        scaff = scaffolding[scaffold_name]
        set_by_dotted_path(scaff.presets, suffix, value)


def distribute_config_updates(prefixes, scaffolding, config_updates):
    for path, value in iterate_flattened(config_updates):
        scaffold_name, suffix = find_best_match(path, prefixes)
        if suffix == "":
            continue
        scaff = scaffolding[scaffold_name]
        set_by_dotted_path(scaff.config_updates, suffix, value)


def distribute_top_down_config_override(top_scaff, prefixes, scaffolding):
    config_updates = top_scaff.config
    for path, value in iterate_flattened(config_updates):
        if top_scaff.path != "":
            path = top_scaff.path + "." + path
        scaffold_name, suffix = find_best_match(path, prefixes)
        scaff = scaffolding[scaffold_name]
        if scaff == top_scaff or suffix == "":
            continue
        update_cfg = {}
        set_by_dotted_path(update_cfg, suffix, value)
        set_by_dotted_path(scaff.config_overrides, suffix, value)
        scaff.config_scopes.append(ConfigDict(update_cfg))
        config_scopes = []
        # apply config before config funcitons that take parameters
        for config in scaff.config_scopes:
            if hasattr(config, "_func") and (len(config.args)>0):
                config_scopes.append(ConfigDict(update_cfg))
            config_scopes.append(config)
        scaff.config_scopes = config_scopes


def get_scaffolding_and_config_name(named_config, scaffolding):
    if os.path.exists(named_config):
        path, cfg_name = "", named_config
    else:
        path, _, cfg_name = named_config.rpartition(".")

        if path not in scaffolding:
            raise KeyError(
                'Ingredient for named config "{}" not found'.format(named_config)
            )
    scaff = scaffolding[path]
    return scaff, cfg_name


def sorted_found_ingredients_dict_by_path(found_dynamic_ingredients):
    return [
        v
        for _, v in sorted(
            found_dynamic_ingredients.items(),
            key=lambda x: len(x[0].split(".")),
            reverse=True,
        )
    ]


def create_run(
    experiment,
    command_name,
    config_updates=None,
    named_configs=(),
    force=False,
    log_level=None,
    include_dynamic_ingredient=True,
    included_dynamic_ingredient=[],
):
    sorted_ingredients = included_dynamic_ingredient + gather_ingredients_topological(
        experiment
    )
    found_dynamic_ingredients = {}
    if include_dynamic_ingredient:
        last_len = -1
        found_dynamic_ingredients_load_paths= {}
        while len(found_dynamic_ingredients) > last_len:
            last_len = len(found_dynamic_ingredients)
            prerun = create_run(
                experiment,
                command_name,
                config_updates,
                named_configs,
                force,
                log_level,
                include_dynamic_ingredient=False,
                included_dynamic_ingredient=sorted_found_ingredients_dict_by_path(
                    found_dynamic_ingredients
                ),
            )
            for cpath, ing in iterate_over_dynamic_ingredients(prerun.config):
                # use relaod to get a new instance of the ingredient, in case you want to use it twice.
                try:
                    ing_module_path = ing.path.rsplit(".", 1)[0]
                    # if it's already imported, make a new instance of the module
                    # this allow importing an ingredient multiple times in different paths.
                    if ing_module_path in sys.modules:
                        del sys.modules[ing_module_path]
                    dyn_ing = getattr(
                        import_module(ing_module_path),
                        ing.path.rsplit(".", 1)[1],
                    )
                except Exception as e:
                    raise RuntimeError(
                        f"Could not dynamically load ingredient specified in config path `{cpath}`. "
                        f"Make sure `{ing.path}` is importable in your python path. "
                        f"This can be tested: `from {ing_module_path} "
                        f"import {ing.path.rsplit('.', 1)[1]}`"
                    ) from e
                dyn_ing.path = cpath
                found_dynamic_ingredients[cpath] = dyn_ing
                found_dynamic_ingredients_load_paths[cpath]=ing.path
        sorted_ingredients = (
            sorted_found_ingredients_dict_by_path(found_dynamic_ingredients)
            + sorted_ingredients
        )

    scaffolding = create_scaffolding(experiment, sorted_ingredients)

    # get all split non-empty prefixes sorted from deepest to shallowest
    prefixes = sorted(
        [s.split(".") for s in scaffolding if s != ""],
        reverse=True,
        key=lambda p: len(p),
    )

    # add dynamic ingredients as sub-subrunners
    # this allows functions captured by the parent to use configurations defined by the son
    for cpath,dyn_ing in found_dynamic_ingredients.items():
        scaffold_name, suffix = find_best_match(".".join(cpath.split(".")[:-1]), prefixes)
        assert scaffolding[scaffold_name].subrunners.get("cpath") is None, f"Undefined behavior, multiple dynamic " \
                                                                           f"ingredients at path {cpath} "
        dyn_scaffold_name, suffix = find_best_match(cpath, prefixes)
        assert dyn_scaffold_name == cpath, f"Failed to find the parent of the dynamic ingredient at path {cpath}"
        scaffolding[scaffold_name].subrunners[cpath] = scaffolding[dyn_scaffold_name]
    # --------- configuration process -------------------

    # Phase 1: Config updates
    config_updates = config_updates or {}
    config_updates = convert_to_nested_dict(config_updates)
    root_logger, run_logger = initialize_logging(experiment, scaffolding, log_level)
    distribute_config_updates(prefixes, scaffolding, config_updates)

    # Report the dynamically created ingredients
    if include_dynamic_ingredient:
        for dyn_ing in sorted_found_ingredients_dict_by_path(found_dynamic_ingredients):
            root_logger.info(
                f"Dynamically created ingredient `{dyn_ing.path}`, loaded from `{found_dynamic_ingredients_load_paths[dyn_ing.path]}` "
            )
    # Phase 2: Named Configs
    for ncfg in named_configs:
        scaff, cfg_name = get_scaffolding_and_config_name(ncfg, scaffolding)
        scaff.gather_fallbacks()
        ncfg_updates = scaff.run_named_config(cfg_name)
        distribute_presets(scaff.path, prefixes, scaffolding, ncfg_updates)
        for ncfg_key, value in iterate_flattened(ncfg_updates):
            set_by_dotted_path(config_updates, join_paths(scaff.path, ncfg_key), value)

    distribute_config_updates(prefixes, scaffolding, config_updates)

    # @ADDED: allow ingredients to override sub ingredients default config
    # Phase extra: propagate configuration down to ingredients
    for scaffold in reversed(list(scaffolding.values())):
        scaffold.gather_fallbacks()
        scaffold.set_up_config()
        distribute_top_down_config_override(scaffold, prefixes, scaffolding)

    # Phase 3: Normal config scopes
    for scaffold in scaffolding.values():
        scaffold.gather_fallbacks()
        scaffold.set_up_config()

        # update global config
        config = get_configuration(scaffolding)
        # run config hooks
        config_hook_updates = scaffold.run_config_hooks(
            config, command_name, run_logger
        )
        recursive_update(scaffold.config, config_hook_updates)

    # Phase 4: finalize seeding
    for scaffold in reversed(list(scaffolding.values())):
        scaffold.set_up_seed()  # partially recursive

    config = get_configuration(scaffolding)
    config_modifications = get_config_modifications(scaffolding)

    # ----------------------------------------------------

    experiment_info = experiment.get_experiment_info()
    host_info = get_host_info(experiment.additional_host_info)
    main_function = get_command(scaffolding, command_name)
    pre_runs = [pr for ing in sorted_ingredients for pr in ing.pre_run_hooks]
    post_runs = [pr for ing in sorted_ingredients for pr in ing.post_run_hooks]

    def get_command_function(command_path):
        return get_command(scaffolding, command_path)

    run = Run(
        config,
        config_modifications,
        main_function,
        copy(experiment.observers),
        root_logger,
        run_logger,
        experiment_info,
        host_info,
        pre_runs,
        post_runs,
        experiment.captured_out_filter,
        get_command_function,
    )

    if hasattr(main_function, "unobserved"):
        run.unobserved = main_function.unobserved

    run.force = force

    for scaffold in scaffolding.values():
        scaffold.finalize_initialization(run=run)
    # finally set current_run
    for ing in sorted_ingredients:
        ing.current_run = run
    return run


def iterate_over_dynamic_ingredients(d):
    """
    Recursively iterate over the items of a dictionary.

    Provides a full dotted paths for every leaf.
    """
    for key in sorted(d.keys()):
        value = d[key]
        # BFS
        if isinstance(value, DynamicIngredient):
            yield key, value
    # second loop for BFS, get ingredients sorted by depth
    for key in sorted(d.keys()):
        value = d[key]
        if isinstance(value, dict) and value:
            for k, v in iterate_over_dynamic_ingredients(d[key]):
                yield join_paths(key, k), v
