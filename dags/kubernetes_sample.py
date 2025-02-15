from datetime import datetime, timedelta

from airflow import DAG
from airflow.contrib.operators.kubernetes_pod_operator import KubernetesPodOperator
from airflow.operators.dummy_operator import DummyOperator

default_args = {
  'owner': 'airflow',
  'depends_on_past': False,
  'start_date': datetime.utcnow(),
  'email': ['airflow@example.com'],
  'email_on_failure': False,
  'email_on_retry': False,
  'retries': 1,
  'retry_delay': timedelta(minutes=5)
}

dag = DAG(
  'kubernetes_sample', default_args=default_args, schedule_interval=timedelta(minutes=10))

start = DummyOperator(task_id='run_this_first', dag=dag)

passing = KubernetesPodOperator(
  namespace='airflow',
  image="python:3.6",
  cmds=["python", "-c"],
  arguments=["print('hello world')"],
  startup_timeout_seconds=180,
  labels={"foo": "bar"},
  name="passing-test",
  task_id="passing-task",
  get_logs=True,
  dag=dag,
  in_cluster=True
)

failing = KubernetesPodOperator(
  namespace='airflow',
  image="ubuntu:18.04",
  cmds=["python", "-c"],
  arguments=["print('hello world')"],
  startup_timeout_seconds=180,
  labels={"foo": "bar"},
  name="fail",
  task_id="failing-task",
  get_logs=True,
  dag=dag,
  in_cluster=True
)

passing.set_upstream(start)
failing.set_upstream(start)
