import sys
import os
import re
import boto3
from botocore.exceptions import ClientError
from gcloud_connectors.bigquery import BigQueryConnector
import fitz
import orjson
import google
import json
from dotenv import load_dotenv
load_dotenv('easytesting/.env')

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')
from easytesting.metrics.bert_score_similarity_check import BertScoreSimilarityCheck
from easytesting.metrics.rouge_similarity_check import RougeSimilarityCheck
from easytesting.test_case import SimilarityTestCase
from easytesting.run_test import assert_test, TestError

s3_client = boto3.client("s3")
ENVIRONMENT = 'test'
os.environ[
    'GOOGLE_APPLICATION_CREDENTIALS'] = '{current_working_directory}/confs/google_cloud_storage_service_account.json'.format(
    current_working_directory=os.getcwd())


reference_text = "Il cane stava correndo nel parco in una giornata di sole, quando all'improvviso scomparve."
old_text = "Il cane è scomparso mentre stava correndo nel parco in una giornata di sole."
new_text = "ciao ciao"


def bert_score_similarity_test(reference_text, old_text, new_text):
    bert_score_similarity_metric = BertScoreSimilarityCheck(minimum_score=0.90)
    test_case = SimilarityTestCase(reference_text=reference_text, old_text=old_text, new_text=new_text,
                                   lang="it", metric_to_use="f1")  # Allowed values: "f1", "precision", "recall"
    try:
        test_result = assert_test(test_case, [bert_score_similarity_metric])
        print(test_result)
        test_result_list = []
        for item in test_result:
            result_dict = {
                "metric": item.metric_name,
                "score": item.score
            }
            test_result_list.append(result_dict)

        return {"test": "success", "scores": test_result_list}
    except TestError as e:
        return {"test": "failed", "error_message": str(e.message)}


import ipdb;ipdb.set_trace()

test = bert_score_similarity_test(reference_text=reference_text, old_text=old_text, new_text=new_text)

import ipdb;ipdb.set_trace()

print(test)

import ipdb;ipdb.set_trace()

def rouge_similarity_test(reference_text, old_text, new_text):
    rouge_similarity_metric = RougeSimilarityCheck(minimum_score=0.50)
    test_case = SimilarityTestCase(reference_text=reference_text, old_text=old_text, new_text=new_text,
                                   metric_to_use="rougeLsum")  # Allowed values: "rouge1", "rouge2", "rougeL", "rougeLsum"
    try:
        test_result = assert_test(test_case, [rouge_similarity_metric])
        print(test_result)
        test_result_list = []
        for item in test_result:
            result_dict = {
                "metric": item.metric_name,
                "score": item.score
            }
            test_result_list.append(result_dict)

        return {"test": "success", "scores": test_result_list}
    except TestError as e:
        return {"test": "failed", "error_message": str(e.message)}

import ipdb;ipdb.set_trace()

test = rouge_similarity_test(reference_text=reference_text, old_text=old_text, new_text=new_text)

import ipdb;ipdb.set_trace()

print(test)

import ipdb;ipdb.set_trace()