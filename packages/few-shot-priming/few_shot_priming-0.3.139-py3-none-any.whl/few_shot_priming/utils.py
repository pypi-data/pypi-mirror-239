def get_experiment_from(args):
    if args.vast:
        experiment = "vast"
    else:
        experiment = "ibmsc"
    return experiment

def get_sampling_strategy_from(args):
    if args.similar_examples:
        sampling_strategy = "similar"
    elif args.diverse_examples:
        sampling_strategy = "diverse"
    else:
        sampling_strategy = None
    return sampling_strategy

def get_similarity_from(args):
    if args.parse_tree_kernel:
        similarity = "parse-tree-kernel"
    elif args.ctm:
        similarity = "ctm"
    elif args.sentence_transformer:
        similarity = "sentence-transformer"
    else:
        raise ValueError("No similarity measure specified!")
    return similarity

def get_experiment_type_from(args):
    if args.validate:
        experiment_type = "validation"
    else:
        experiment_type= "test"
    return experiment_type

def get_model_name(config):
    model_name = config["model-name"]
    return model_name

def get_run_name(args, config, prompting_type):
    experiment = get_experiment_from(args)
    experiment_type = get_experiment_type_from(args)
    sampling_strategy = get_sampling_strategy_from(args)
    if sampling_strategy:
        similarity = get_similarity_from(args)

    model_name = get_model_name(config)
    if args.optimize:
        run = "optimize-hyperparameters"
    elif args.analyze_k:
        run = "analzye-k"
    else:
        run = None
    if sampling_strategy:
        if run:
            results_name = f"{prompting_type}-{experiment}-{experiment_type}-{model_name}-{run}-{sampling_strategy}-{similarity}"
        else:
            results_name = f"{prompting_type}-{experiment}-{experiment_type}-{model_name}-{sampling_strategy}-{similarity}"
    else:
        if run:
            results_name = f"{prompting_type}-{experiment}-{experiment_type}-{model_name}-{run}"
        else:
            results_name = f"{prompting_type}-{experiment}-{experiment_type}-{model_name}"

    return results_name


def init_wandb(offline=False, config=None, params=None):
    if offline:
        os.environ['WANDB_MODE'] = 'offline'

    wandb.login(relogin=True)
    wandb.init(project="prompt-fine-tuning-alpaca")


