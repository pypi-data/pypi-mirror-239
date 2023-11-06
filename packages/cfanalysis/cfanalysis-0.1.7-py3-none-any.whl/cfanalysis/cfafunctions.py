import numpy as np
import pandas as pd
import itertools

from tdc.single_pred import ADME
from tdc.benchmark_group import admet_group
from tdc import BenchmarkGroup
from tdc import Evaluator

# convert predicted probabilities for classification sets to score
def pred_prob_to_score(pred_prob):
    res = []
    for i in range(len(pred_prob)):
        res.append(pred_prob[i][1])
    res = np.array(res)
    return res

# normalization of scores
def normalize(array): # define function for normalization of scores
  maximum = np.max(array)
  minimum = np.min(array)
  norm_list = []
  for i in range(len(array)):
      norm_list.append((array[i]-minimum)/(maximum-minimum))
  return np.array(norm_list)

# convert df to a list
def df_to_list(df):
  res = []
  for col in df.columns:
    res.append(df[col].to_numpy())
  return res

# input model predictions and model names
def model_predictions(numberofmodels, modelnames, val_dfs_list, test_dfs_list):
    # Check if the number of provided DataFrames matches the expected number
    if len(val_dfs_list) != numberofmodels:
        raise ValueError(f"Expected {numberofmodels} lists of DataFrames (one for each ML model) for validation, but {len(val_dfs_list)} were provided.")
    if len(test_dfs_list) != numberofmodels:
        raise ValueError(f"Expected {numberofmodels} lists of DataFrames (one for each ML model) for testing, but {len(test_dfs_list)} were provided.")

    valpredictions_modelnames = {}
    testpredictions_modelnames = {}

    # Process validation DataFrames
    for i, df in enumerate(val_dfs_list):
        model_name = modelnames[i]
        valpredictions_modelnames[f'predictions_val_{model_name}'] = df_to_list(df)
 
    # Process test DataFrames
    for i, df in enumerate(test_dfs_list):
        model_name = modelnames[i]
        testpredictions_modelnames[f'predictions_test_{model_name}'] = df_to_list(df)
        
    return valpredictions_modelnames, testpredictions_modelnames

def get_auroc(y_pred_proba, y_true):
  evaluator = Evaluator(name = 'ROC-AUC')
  res = evaluator(y_true, y_pred_proba)
  #res = metrics.roc_auc_score(y_true, y_pred_proba)
  return res

def get_auprc(y_pred_proba, y_true):
  evaluator = Evaluator(name = 'PR-AUC')
  res = evaluator(y_true, y_pred_proba)
  return res

def get_spearman_corr(y_pred_rank, y_true_rank):
  evaluator = Evaluator(name = 'Spearman')
  res = evaluator(y_true_rank, y_pred_rank)
  return res
def score_to_rank(array):
  res = np.argsort(np.flip(np.argsort(array)))+1
  return res

def get_mae(y_pred, y_true):
  evaluator = Evaluator(name = 'MAE')
  res = evaluator(y_true,y_pred)
  return res

def powerset(s):
    x = len(s)
    ls = []
    for i in range(1 << x):
        ls.append([s[j] for j in range(x) if (i & (1 << j))])
    return ls[1:]

def generate_models_list(model_names):
    models = powerset(model_names)

    def myFunc(e):
        return len(e)

    models.sort(key=myFunc)

    models_list = []

    for i in range(len(models)):
        if len(models[i]) > 0:
            combination = "&".join(models[i])
            models_list.append(combination)

    return models_list

def calculate_aurocscores(model_names, preds, y_valid):
    ps_score = [[] for _ in range(5)]  # Initialize ps_score outside the loop
    for sys in model_names:
        for seed in [1, 2, 3, 4, 5]:
            predictions_val = preds[0][f'predictions_val_{sys}'][seed - 1]  # Adjust for zero-based indexing
            y_val = y_valid[seed]

            n = len(predictions_val[~np.isnan(predictions_val)])
            m = len(y_val)
            if n >= m:
                ps = get_auroc(predictions_val[:m], y_val)
            else:
                ps = get_auroc(predictions_val[~np.isnan(predictions_val)], y_val[:n])
            ps_score[seed - 1].append(ps)  # Subtract 1 to adjust for zero-based indexing
    ds_score = [[] for _ in range(5)]
    for sys in model_names:
            for seed in [1, 2, 3, 4, 5]:
                loc = model_names.index(sys)
                model_names.remove(sys)
                ds = 0
                for i in range(len(model_names)-1):
                    sys_key = f'predictions_val_{sys}'
                    model_key = f'predictions_val_{model_names[i]}'
                    ds += np.sum(np.square(normalize(np.sort(preds[0][sys_key][seed-1])) - normalize(np.sort(preds[0][model_key][seed-1]))))
                ds = ds / len(model_names)
                model_names.insert(loc, sys)
                ds_score[seed-1].append(ds)

    ds_rank = np.reciprocal(ds_score)
    return ds_score, ds_rank, ps_score

def calculate_auprcscores(model_names, preds, y_valid):
    ps_score = [[] for _ in range(5)]  # Initialize ps_score outside the loop
    for sys in model_names:
        for seed in [1, 2, 3, 4, 5]:
            predictions_val = preds[0][f'predictions_val_{sys}'][seed - 1]  # Adjust for zero-based indexing
            y_val = y_valid[seed]

            n = len(predictions_val[~np.isnan(predictions_val)])
            m = len(y_val)
            if n >= m:
                ps = get_auprc(predictions_val[:m], y_val)
            else:
                ps = get_auprc(predictions_val[~np.isnan(predictions_val)], y_val[:n])
            ps_score[seed - 1].append(ps)  # Subtract 1 to adjust for zero-based indexing
    ds_score = [[] for _ in range(5)]
    for sys in model_names:
            for seed in [1, 2, 3, 4, 5]:
                loc = model_names.index(sys)
                model_names.remove(sys)
                ds = 0
                for i in range(len(model_names)-1):
                    sys_key = f'predictions_val_{sys}'
                    model_key = f'predictions_val_{model_names[i]}'
                    ds += np.sum(np.square(normalize(np.sort(preds[0][sys_key][seed-1])) - normalize(np.sort(preds[0][model_key][seed-1]))))
                ds = ds / len(model_names)
                model_names.insert(loc, sys)
                ds_score[seed-1].append(ds)

    ds_rank = np.reciprocal(ds_score)
    return ds_score, ds_rank, ps_score
    
def calculate_maescores(model_names, preds, y_valid):
    ps_score = [[] for _ in range(5)]  # Initialize ps_score outside the loop
    for sys in model_names:
        for seed in [1, 2, 3, 4, 5]:
            predictions_val = preds[0][f'predictions_val_{sys}'][seed - 1]  # Adjust for zero-based indexing
            y_val = y_valid[seed]

            n = len(predictions_val[~np.isnan(predictions_val)])
            m = len(y_val)
            if n >= m:
                ps = get_mae(predictions_val[:m], y_val)
            else:
                ps = get_mae(predictions_val[~np.isnan(predictions_val)], y_val[:n])
            ps_score[seed - 1].append(ps)  # Subtract 1 to adjust for zero-based indexing

    ds_score = [[] for _ in range(5)]
    for sys in model_names:
            for seed in [1, 2, 3, 4, 5]:
                loc = model_names.index(sys)
                model_names.remove(sys)
                ds = 0
                for i in range(len(model_names)-1):
                    sys_key = f'predictions_val_{sys}'
                    model_key = f'predictions_val_{model_names[i]}'
                    ds += np.sum(np.square(normalize(np.sort(preds[0][sys_key][seed-1])) - normalize(np.sort(preds[0][model_key][seed-1]))))
                ds = ds / len(model_names)
                model_names.insert(loc, sys)
                ds_score[seed-1].append(ds)

    ds_rank = np.reciprocal(ds_score)
    return ds_score, ds_rank, ps_score

def calculate_spearmanscores(model_names, preds, y_valid):
    ps_score = [[] for _ in range(5)]  # Initialize ps_score outside the loop
    for sys in model_names:
        for seed in [1, 2, 3, 4, 5]:
            predictions_val = preds[0][f'predictions_val_{sys}'][seed - 1]  # Adjust for zero-based indexing
            y_val = y_valid[seed]

            n = len(predictions_val[~np.isnan(predictions_val)])
            m = len(y_val)
            if n >= m:
                ps = get_spearman_corr(score_to_rank(predictions_val[:m]), score_to_rank(y_val))
            else:
                ps = get_spearman_corr(score_to_rank(predictions_val[~np.isnan(predictions_val)]), score_to_rank(y_val[:n]))
            ps_score[seed - 1].append(ps)  # Subtract 1 to adjust for zero-based indexing

    ds_score = [[] for _ in range(5)]
    for sys in model_names:
            for seed in [1, 2, 3, 4, 5]:
                loc = model_names.index(sys)
                model_names.remove(sys)
                ds = 0
                for i in range(len(model_names)-1):
                    sys_key = f'predictions_val_{sys}'
                    model_key = f'predictions_val_{model_names[i]}'
                    ds += np.sum(np.square(normalize(np.sort(preds[0][sys_key][seed-1])) - normalize(np.sort(preds[0][model_key][seed-1]))))
                ds = ds / len(model_names)
                model_names.insert(loc, sys)
                ds_score[seed-1].append(ds)

    ds_rank = np.reciprocal(ds_score)
    return ds_score, ds_rank, ps_score

# perform avg score combinations
def create_avg_score_combine(seed, model_names, preds):
    avg_score_combine = pd.DataFrame()
    
    # Create combinations of model names separated by "&"
    all_combinations = []
    for r in range(1, len(model_names) + 1):
        combinations = itertools.combinations(model_names, r)
        all_combinations.extend(['&'.join(combination) for combination in combinations])
    
    # Add individual models to the list
    all_combinations.extend(model_names)
    
    for combination in all_combinations:
        models = combination.split('&')
        avg_preds = sum(preds[1][f'predictions_test_{model_name}'][seed - 1] for model_name in models) / len(models)
        avg_score_combine[combination] = avg_preds
    
    return avg_score_combine

# perform avg rank combinations
def create_avg_rank_combine(seed, model_names, preds):
    avg_rank_combine = pd.DataFrame({model_name: score_to_rank(preds[1][f'predictions_test_{model_name}'])[seed - 1] for model_name in model_names})
    return avg_rank_combine

def avg_rank_combine(models_list, single_rank):
    for j in models_list[len(model_names):]:
        split_j = j.split('&')
        num_elements = len(split_j)
        if num_elements > 1:
            avg_rank = sum(single_rank[element] for element in split_j) / num_elements
            single_rank[j + '_r'] = avg_rank

# perform weighted score combination by diversity strength
def ds_score_combine(models_list, single_score, ds_score_combine, ds_score, model_names):
    for j in models_list[len(model_names):]:
        elements = j.split('&')
        num_elements = len(elements)
        
        numerator = 0
        denominator = 0

        for element in elements:
            element_index = model_names.index(element)
            numerator += single_score[element] * ds_score[element_index]
            denominator += ds_score[element_index]

        ds_score_combine[j + '_ds'] = numerator / denominator

# perform weighted rank combination by diversity strength
def ds_rank_combine(models_list, single_rank, ds_rank_combine, ds_rank, model_names):
    for j in models_list[len(model_names):]:
        elements = j.split('&')
        num_elements = len(elements)
        
        numerator = 0
        denominator = 0

        for element in elements:
            element_index = model_names.index(element)
            numerator += single_rank[element] * ds_rank[element_index]
            denominator += ds_rank[element_index]

        ds_rank_combine[j + '_ds_r'] = numerator / denominator

# perform weighted score combination by performance strength 
def ps_score_combine(models_list, single_score, ps_score_combine, ps_score, model_names):
    for j in models_list[len(model_names):]:
        elements = j.split('&')
        num_elements = len(elements)

        numerator = 0
        denominator = 0

        for element in elements:
            element_index = model_names.index(element)
            numerator += single_score[element] / ps_score[element_index]
            denominator += 1 / ps_score[element_index]

        ps_score_combine[j + '_ps'] = numerator / denominator

# perform weighted rank combination by performance strength
def ps_rank_combine(models_list, single_rank, ps_rank_combine, ps_score, model_names):
    for j in models_list[len(model_names):]:
        elements = j.split('&')
        num_elements = len(elements)

        numerator = 0
        denominator = 0

        for element in elements:
            element_index = model_names.index(element)
            numerator += single_rank[element] * ps_score[element_index]
            denominator += ps_score[element_index]

        ps_rank_combine[j + '_ps_r'] = numerator / denominator

# get mae for all the models and model combinations
def calculate_MAE(model_names, preds, y_test, y_valid):
    seed_values = [1, 2, 3, 4, 5]
    avg_score_combine_seeds = []
    avg_rank_combine_seeds = []
    ds_score_combine_seeds = []
    ds_rank_combine_seeds = []
    ps_score_combine_seeds = []
    ps_rank_combine_seeds = []

    for seed in seed_values:
        avg_score_combine_seed = create_avg_score_combine(seed, model_names, preds)
        avg_score_combine_seeds.append(avg_score_combine_seed)
        avg_rank_combine_seed = create_avg_rank_combine(seed, model_names, preds)
        avg_rank_combine_seeds.append(avg_rank_combine_seed)

        ds_score_combine_seed = pd.DataFrame()
        ds_rank_combine_seed = pd.DataFrame()
        ps_score_combine_seed = pd.DataFrame()
        ps_rank_combine_seed = pd.DataFrame()

        ds_scores, ps_scores = calculate_maescores(model_names, preds, y_valid)[0], calculate_maescores(model_names, preds, y_valid)[2]
        ds_score_combine(generate_models_list(model_names), avg_score_combine_seed, ds_score_combine_seed, ds_scores[seed - 1], model_names)
        ds_rank_combine(generate_models_list(model_names), avg_rank_combine_seed, ds_rank_combine_seed, ds_scores[seed - 1], model_names)
        ps_score_combine(generate_models_list(model_names), avg_score_combine_seed, ps_score_combine_seed, ps_scores[seed - 1], model_names)
        ps_rank_combine(generate_models_list(model_names), avg_rank_combine_seed, ps_rank_combine_seed, ps_scores[seed - 1], model_names)

        ds_score_combine_seeds.append(ds_score_combine_seed)
        ds_rank_combine_seeds.append(ds_rank_combine_seed)
        ps_score_combine_seeds.append(ps_score_combine_seed)
        ps_rank_combine_seeds.append(ps_rank_combine_seed)

    score_combine_list = np.hstack((np.array(avg_score_combine_seeds[0].columns), np.array(ds_score_combine_seeds[0].columns), np.array(ps_score_combine_seeds[0].columns)))
    MAE = pd.DataFrame(index=score_combine_list)

    for i in range(1, 6):
        mae_avg, mae_ds, mae_ps = [], [], []
        for col in avg_score_combine_seeds[i - 1].columns:
            mae = get_mae(np.array(avg_score_combine_seeds[i - 1][col]), y_test)
            mae_avg.append(mae)
        for col in ds_score_combine_seeds[i - 1].columns:
            mae = get_mae(np.array(ds_score_combine_seeds[i - 1][col]), y_test)
            mae_ds.append(mae)
        for col in ps_score_combine_seeds[i - 1].columns:
            mae = get_mae(np.array(ps_score_combine_seeds[i - 1][col]), y_test)
            mae_ps.append(mae)
        MAE['seed' + str(i)] = np.hstack((mae_avg, mae_ds, mae_ps))
    MAE['avg_MAE'] = MAE.mean(axis=1)
    MAE.sort_values(by='avg_MAE', inplace=True)
    return MAE
    
# get spearman corr for all the models and model combinations
def calculate_spearman_corr(model_names, preds, y_test, y_valid):
    y_test_rank = score_to_rank(y_test)
    
    seed_values = [1, 2, 3, 4, 5]
    avg_score_combine_seeds = []
    avg_rank_combine_seeds = []
    ds_score_combine_seeds = []
    ds_rank_combine_seeds = []
    ps_score_combine_seeds = []
    ps_rank_combine_seeds = []

    for seed in seed_values:
        avg_score_combine_seed = create_avg_score_combine(seed, model_names, preds)
        avg_score_combine_seeds.append(avg_score_combine_seed)
        avg_rank_combine_seed = create_avg_rank_combine(seed, model_names, preds)
        avg_rank_combine_seeds.append(avg_rank_combine_seed)

        ds_score_combine_seed = pd.DataFrame()
        ds_rank_combine_seed = pd.DataFrame()
        ps_score_combine_seed = pd.DataFrame()
        ps_rank_combine_seed = pd.DataFrame()

        ds_scores, ps_scores = calculate_spearmanscores(model_names, preds, y_valid)[0], calculate_spearmanscores(model_names, preds, y_valid)[2]
        ds_score_combine(generate_models_list(model_names), avg_score_combine_seed, ds_score_combine_seed, ds_scores[seed - 1], model_names)
        ds_rank_combine(generate_models_list(model_names), avg_rank_combine_seed, ds_rank_combine_seed, ds_scores[seed - 1], model_names)
        ps_score_combine(generate_models_list(model_names), avg_score_combine_seed, ps_score_combine_seed, ps_scores[seed - 1], model_names)
        ps_rank_combine(generate_models_list(model_names), avg_rank_combine_seed, ps_rank_combine_seed, ps_scores[seed - 1], model_names)

        ds_score_combine_seeds.append(ds_score_combine_seed)
        ds_rank_combine_seeds.append(ds_rank_combine_seed)
        ps_score_combine_seeds.append(ps_score_combine_seed)
        ps_rank_combine_seeds.append(ps_rank_combine_seed)
        
    seed_dfs = [avg_rank_combine_seeds[0], avg_rank_combine_seeds[1], avg_rank_combine_seeds[2], avg_rank_combine_seeds[3], avg_rank_combine_seeds[4]]
    for seed_df in seed_dfs:
        columns_to_rename = [col for col in seed_df.columns if not col.endswith('_r')]
        seed_df.rename(columns={col: col + '_r' for col in columns_to_rename}, inplace=True)

    rank_combine_list = np.hstack((np.array(avg_rank_combine_seeds[0].columns), np.array(ds_rank_combine_seeds[0].columns), np.array(ps_rank_combine_seeds[0].columns)))
    spearman_corr = pd.DataFrame(index=rank_combine_list)

    for i in range(1, 6):
        sc_avg, sc_ds, sc_ps = [], [], []
        for col in avg_rank_combine_seeds[i - 1].columns:
            sc = get_spearman_corr(np.array(avg_rank_combine_seeds[i - 1][col]), y_test_rank)
            sc_avg.append(sc)
        for col in ds_rank_combine_seeds[i - 1].columns:
            sc = get_spearman_corr(np.array(ds_rank_combine_seeds[i - 1][col]), y_test_rank)
            sc_ds.append(sc)
        for col in ps_rank_combine_seeds[i - 1].columns:
            sc = get_spearman_corr(np.array(ps_rank_combine_seeds[i - 1][col]), y_test_rank)
            sc_ps.append(sc)
        spearman_corr['seed' + str(i)] = np.hstack((sc_avg, sc_ds, sc_ps))

    spearman_corr['avg_spearman'] = spearman_corr.mean(axis=1)
    spearman_corr.sort_values(by='avg_spearman', ascending=False, inplace=True)
    return spearman_corr
    
# get auroc for all the models and model combinations
def calculate_auroc(model_names, preds, y_test, y_valid):
    seed_values = [1, 2, 3, 4, 5]
    avg_score_combine_seeds = []
    avg_rank_combine_seeds = []
    ds_score_combine_seeds = []
    ds_rank_combine_seeds = []
    ps_score_combine_seeds = []
    ps_rank_combine_seeds = []

    for seed in seed_values:
        avg_score_combine_seed = create_avg_score_combine(seed, model_names, preds)
        avg_score_combine_seeds.append(avg_score_combine_seed)
        avg_rank_combine_seed = create_avg_rank_combine(seed, model_names, preds)
        avg_rank_combine_seeds.append(avg_rank_combine_seed)

        ds_score_combine_seed = pd.DataFrame()
        ds_rank_combine_seed = pd.DataFrame()
        ps_score_combine_seed = pd.DataFrame()
        ps_rank_combine_seed = pd.DataFrame()

        ds_scores, ps_scores = calculate_aurocscores(model_names, preds, y_valid)[0], calculate_aurocscores(model_names, preds, y_valid)[2]
        ds_score_combine(generate_models_list(model_names), avg_score_combine_seed, ds_score_combine_seed, ds_scores[seed - 1], model_names)
        ds_rank_combine(generate_models_list(model_names), avg_rank_combine_seed, ds_rank_combine_seed, ds_scores[seed - 1], model_names)
        ps_score_combine(generate_models_list(model_names), avg_score_combine_seed, ps_score_combine_seed, ps_scores[seed - 1], model_names)
        ps_rank_combine(generate_models_list(model_names), avg_rank_combine_seed, ps_rank_combine_seed, ps_scores[seed - 1], model_names)

        ds_score_combine_seeds.append(ds_score_combine_seed)
        ds_rank_combine_seeds.append(ds_rank_combine_seed)
        ps_score_combine_seeds.append(ps_score_combine_seed)
        ps_rank_combine_seeds.append(ps_rank_combine_seed)

    score_combine_list = np.hstack((np.array(avg_score_combine_seeds[0].columns), np.array(ds_score_combine_seeds[0].columns), np.array(ps_score_combine_seeds[0].columns)))
    AUROC = pd.DataFrame(index=score_combine_list)

    for i in range(1, 6):
        auroc_avg, auroc_ds, auroc_ps = [], [], []
        for col in avg_score_combine_seeds[i - 1].columns:
            auroc = get_auroc(np.array(avg_score_combine_seeds[i - 1][col]), y_test)
            auroc_avg.append(auroc)
        for col in ds_score_combine_seeds[i - 1].columns:
            auroc = get_auroc(np.array(ds_score_combine_seeds[i - 1][col]), y_test)
            auroc_ds.append(auroc)
        for col in ps_score_combine_seeds[i - 1].columns:
            auroc = get_auroc(np.array(ps_score_combine_seeds[i - 1][col]), y_test)
            auroc_ps.append(auroc)
        AUROC['seed' + str(i)] = np.hstack((auroc_avg, auroc_ds, auroc_ps))
    AUROC['avg_AUROC'] = AUROC.mean(axis=1)
    AUROC.sort_values(by='avg_AUROC', ascending=False, inplace=True)
    return AUROC,len(score_combine_list)

# get auroc for all the models and model combinations
def calculate_auprc(model_names, preds, y_test, y_valid):
    seed_values = [1, 2, 3, 4, 5]
    avg_score_combine_seeds = []
    avg_rank_combine_seeds = []
    ds_score_combine_seeds = []
    ds_rank_combine_seeds = []
    ps_score_combine_seeds = []
    ps_rank_combine_seeds = []

    for seed in seed_values:
        avg_score_combine_seed = create_avg_score_combine(seed, model_names, preds)
        avg_score_combine_seeds.append(avg_score_combine_seed)
        avg_rank_combine_seed = create_avg_rank_combine(seed, model_names, preds)
        avg_rank_combine_seeds.append(avg_rank_combine_seed)

        ds_score_combine_seed = pd.DataFrame()
        ds_rank_combine_seed = pd.DataFrame()
        ps_score_combine_seed = pd.DataFrame()
        ps_rank_combine_seed = pd.DataFrame()

        ds_scores, ps_scores = calculate_auprcscores(model_names, preds, y_valid)[0], calculate_auprcscores(model_names, preds, y_valid)[2]
        ds_score_combine(generate_models_list(model_names), avg_score_combine_seed, ds_score_combine_seed, ds_scores[seed - 1], model_names)
        ds_rank_combine(generate_models_list(model_names), avg_rank_combine_seed, ds_rank_combine_seed, ds_scores[seed - 1], model_names)
        ps_score_combine(generate_models_list(model_names), avg_score_combine_seed, ps_score_combine_seed, ps_scores[seed - 1], model_names)
        ps_rank_combine(generate_models_list(model_names), avg_rank_combine_seed, ps_rank_combine_seed, ps_scores[seed - 1], model_names)

        ds_score_combine_seeds.append(ds_score_combine_seed)
        ds_rank_combine_seeds.append(ds_rank_combine_seed)
        ps_score_combine_seeds.append(ps_score_combine_seed)
        ps_rank_combine_seeds.append(ps_rank_combine_seed)

    score_combine_list = np.hstack((np.array(avg_score_combine_seeds[0].columns), np.array(ds_score_combine_seeds[0].columns), np.array(ps_score_combine_seeds[0].columns)))
    AUPRC = pd.DataFrame(index=score_combine_list)

    for i in range(1, 6):
        auprc_avg, auprc_ds, auprc_ps = [], [], []
        for col in avg_score_combine_seeds[i - 1].columns:
            auprc = get_auprc(np.array(avg_score_combine_seeds[i - 1][col]), y_test)
            auprc_avg.append(auprc)
        for col in ds_score_combine_seeds[i - 1].columns:
            auprc = get_auprc(np.array(ds_score_combine_seeds[i - 1][col]), y_test)
            auprc_ds.append(auprc)
        for col in ps_score_combine_seeds[i - 1].columns:
            auprc = get_auprc(np.array(ps_score_combine_seeds[i - 1][col]), y_test)
            auprc_ps.append(auprc)
        AUPRC['seed' + str(i)] = np.hstack((auprc_avg, auprc_ds, auprc_ps))
    AUPRC['avg_AUPRC'] = AUPRC.mean(axis=1)
    AUPRC.sort_values(by='avg_AUPRC', ascending=False, inplace=True)
    return AUPRC

