
import time
import tracemalloc
import pandas as pd
import numpy as np
from typing import Union

from dtaianomaly.data_management import DataManager
from dtaianomaly.anomaly_detection.utility.TrainType import TrainType

from dtaianomaly.visualization.plot_anomalies import plot_anomaly_scores

from dtaianomaly.workflow.handle_data_configuration import DataConfiguration, handle_data_configuration
from dtaianomaly.workflow.handle_algorithm_configuration import AlgorithmConfiguration, handle_algorithm_configuration
from dtaianomaly.workflow.handle_metric_configuration import MetricConfiguration, handle_metric_configuration
from dtaianomaly.workflow.handle_output_configuration import PlainOutputConfiguration, OutputConfiguration, handle_output_configuration


def __log(message: str, print_message: bool) -> None:
    if print_message:
        print(message)


def main(data_manager: DataManager,
         data_configuration: DataConfiguration,
         algorithm_configuration: AlgorithmConfiguration,
         metric_configuration: MetricConfiguration,
         output_configuration: Union[PlainOutputConfiguration, OutputConfiguration]) -> pd.DataFrame:
    """
    Execute an anomaly detector.

    :param data_manager:
    :param data_configuration:
    :param algorithm_configuration:
    :param metric_configuration:
    :param output_configuration:

    :return:
    """
    data_manager = handle_data_configuration(data_manager, data_configuration)
    algorithm, algorithm_name = handle_algorithm_configuration(algorithm_configuration)
    algorithm_train_type = algorithm.train_type()
    metrics = handle_metric_configuration(metric_configuration)
    output_configuration = handle_output_configuration(output_configuration, algorithm_name)

    __log(message='>>> Starting the workflow',
          print_message=output_configuration.verbose)

    results_columns = list(metrics.keys())
    if output_configuration.trace_time:
        results_columns += ['Time fit (s)', 'Time predict (s)']
    if output_configuration.trace_memory:
        results_columns += ['Peak memory fit (KiB)', 'Peak memory predict (KiB)']
    results = pd.DataFrame(
        index=pd.MultiIndex.from_tuples(data_manager.get(), names=['collection_name', 'dataset_name']),
        columns=results_columns
    )

    __log(message=f">>> Iterating over the datasets\n"
                  f"Total number of datasets: {len(data_manager.get())}",
          print_message=output_configuration.verbose)
    for dataset_index in data_manager.get():
        __log(message=f">>> Handling dataset '{dataset_index}'",
              print_message=output_configuration.verbose)

        __log(message=f">> Checking  algorithm-dataset compatibility",
              print_message=output_configuration.verbose)
        meta_data = data_manager.get_metadata(dataset_index)
        if not algorithm_train_type.can_solve_train_type_data(meta_data['train_type']):
            __log(message=f"The algorithm is not compatible with dataset {dataset_index}\n"
                          f"Algorithm type: {algorithm_train_type}\n"
                          f"Dataset type: {meta_data['train_type']}\n"
                          f"An error will be raised: {output_configuration.invalid_train_type_raise_error}",
                  print_message=output_configuration.verbose)
            if output_configuration.invalid_train_type_raise_error:
                raise Exception(f"Algorithm type '{algorithm_train_type}' can not solve dataset type '{meta_data['train_type']}'!")
            else:
                results.loc[dataset_index] = pd.Series(index=results_columns)
                continue

        __log(message=f">> Loading the train data",
              print_message=output_configuration.verbose)
        # For supervised algorithms, the ground truth of the train data is required
        if algorithm_train_type == TrainType.SUPERVISED:
            __log(message=f"Using train data and labels for supervised algorithm",
                  print_message=output_configuration.verbose)
            data_train, ground_truth_train = data_manager.load_raw_data(dataset_index, train=True)

        # For semi-supervised algorithms, train data is required but not its ground truth, because
        # semi-supervised algorithms assume that the given data is normal
        elif algorithm_train_type == TrainType.SEMI_SUPERVISED:
            __log(message=f"Using train data but no labels for semi-supervised algorithm",
                  print_message=output_configuration.verbose)
            data_train, _ = data_manager.load_raw_data(dataset_index, train=True)
            ground_truth_train = None

        # For unsupervised algorithms, use the train data to fit, if available, and otherwise use
        # the test data, but no labels are provided
        else:
            if meta_data['train_type'] == 'unsupervised':
                __log(message=f"Using **test** data but no labels for unsupervised algorithm",
                      print_message=output_configuration.verbose)
                data_train, _ = data_manager.load_raw_data(dataset_index, train=False)
            else:
                __log(message=f"Using train data but no labels for unsupervised algorithm",
                      print_message=output_configuration.verbose)
                data_train, _ = data_manager.load_raw_data(dataset_index, train=True)
            ground_truth_train = None

        # Initialize the memory tracing variables to avoid warnings
        peak_memory_fitting = np.nan
        peak_memory_predicting = np.nan

        # Fit the algorithm
        __log(message=f">> Fitting the algorithm",
              print_message=output_configuration.verbose)
        if output_configuration.trace_memory:
            tracemalloc.start()
        start_fitting = time.time()
        algorithm.fit(data_train, ground_truth_train)
        time_fitting = time.time() - start_fitting
        if output_configuration.trace_memory:
            _, peak_memory_fitting = tracemalloc.get_traced_memory()
            tracemalloc.stop()

        # Read the test data
        __log(message=f">> Loading the test data",
              print_message=output_configuration.verbose)
        data_test, ground_truth_test = data_manager.load_raw_data(dataset_index, train=False)

        # Predict the decision scores
        __log(message=f">> Predicting the decision scores on the test data",
              print_message=output_configuration.verbose)
        if output_configuration.trace_memory:
            tracemalloc.start()
        start_predicting = time.time()
        # decision_function instead of predict_proba to not include normalization time
        # Additionally, the scores are cached to avoid recomputing them.
        algorithm.decision_function(data_test)
        time_predicting = time.time() - start_predicting
        if output_configuration.trace_memory:
            _, peak_memory_predicting = tracemalloc.get_traced_memory()
            tracemalloc.stop()

        # Write away the results
        __log(message=f">> Storing the results",
              print_message=output_configuration.verbose)
        __log(message=f"Computing the evaluation metrics metrics",
              print_message=output_configuration.verbose)
        predicted_proba = algorithm.predict_proba(data_test)
        for metric_name, metric in metrics.items():
            __log(message=f"Computing the evaluation metric '{metric_name}'",
                  print_message=output_configuration.verbose)
            results.at[dataset_index, metric_name] = metric.compute(ground_truth_test, predicted_proba)
            __log(message=f"Evaluation: '{results.at[dataset_index, metric_name]}'",
                  print_message=output_configuration.verbose)
        if output_configuration.trace_time:
            __log(message=f"Saving the timing information",
                  print_message=output_configuration.verbose)
            results.at[dataset_index, 'Time fit (s)'] = np.round(time_fitting, 5)
            results.at[dataset_index, 'Time predict (s)'] = np.round(time_predicting, 5)
        if output_configuration.trace_memory:
            __log(message=f"Saving the memory usage",
                  print_message=output_configuration.verbose)
            results.at[dataset_index, 'Peak memory fit (KiB)'] = np.round(peak_memory_fitting / 1024, 5)
            results.at[dataset_index, 'Peak memory predict (KiB)'] = np.round(peak_memory_predicting / 1024, 5)

        # Save the anomaly scores plot, if requested
        if output_configuration.save_anomaly_scores_plot:
            __log(message=f">> Saving the anomaly score plot\n"
                          f"path: {output_configuration.figure_path(dataset_index)}\n"
                          f"format: {output_configuration.anomaly_scores_file_format}\n"
                          f"show_anomaly_scores: {output_configuration.show_anomaly_scores}\n"
                          f"show_ground_truth: {output_configuration.show_ground_truth}",
                  print_message=output_configuration.verbose)
            plot_anomaly_scores(
                trend_data=data_manager.load(dataset_index),
                anomaly_scores=algorithm.decision_function(data_test),
                file_path=output_configuration.figure_path(dataset_index),
                show_anomaly_scores=output_configuration.show_anomaly_scores,
                show_ground_truth=output_configuration.show_ground_truth
            )

        # Save the results after each iteration, if requested
        if output_configuration.save_results and output_configuration.constantly_save_results:
            __log(message=f">>> Saving the results to disk\n"
                          f"path: {output_configuration.results_path}",
                  print_message=output_configuration.verbose)
            results.to_csv(output_configuration.results_path)

    # Save the results, if requested
    if output_configuration.save_results:
        __log(message=f">>> Saving the results to disk\n"
                      f"path: {output_configuration.results_path}",
              print_message=output_configuration.verbose)
        results.to_csv(output_configuration.results_path)

    if output_configuration.print_results:
        __log(message=f">>> Printing the results to the output stream",
              print_message=output_configuration.verbose)
        print(results)

    return results
