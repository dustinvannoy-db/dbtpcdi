
def model(dbt, session):
    dbt.config(
        submission_method='workflow_job',
        timeout=300, 
        python_job_config = {
            "budget_policy_id": "d954df15-71b7-48ce-9db8-10aa0443173c", 
            "tags": {"workflow_dbt_project": "dbtpcdi"},
            "performance_target": "PERFORMANCE_OPTIMIZED",
            "name":"dbt_customer3"
        })
        # environment_key="my_env",
        # environment_dependencies=["faker==37.0.2"],
        # python_job_config = {
        #     "name":"dbt_customer3_job2", "budget_policy_id": "d954df15-71b7-48ce-9db8-10aa0443173c", 
        #     "tags": {"dbt_project": "dbtpcdi"}, "performance_target": "PERFORMANCE_OPTIMIZED", 
        #     "environments": [
        #     {
        #     "environment_key": "my_env",
        #     "spec": {
        #         "client": "1",
        #         "dependencies": [
        #             "faker==37.0.2"
        #         ]
        #         }
        #     }]
        # },
        # additional_task_settings = {"task_key": "my_python_Customer3"}

    my_sql_model_df = dbt.ref("CustomerIncremental")

    final_df = my_sql_model_df.selectExpr("*").limit(100)

    return final_df

