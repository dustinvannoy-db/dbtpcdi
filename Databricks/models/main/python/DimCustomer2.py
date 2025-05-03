from faker import Faker


def model(dbt, session):
    dbt.config(submission_method='serverless_cluster', timeout=300, 
               environment_key="my_env",
               environment_dependencies=["faker==37.0.2"],
               python_job_config = {"budget_policy_id": "d954df15-71b7-48ce-9db8-10aa0443173c", 
                                    "tags": {"runsubmit_dbt_project": "dbtpcdi"},
                                }
    )

    my_sql_model_df = dbt.ref("CustomerIncremental")

    fake = Faker()

    print(fake.name())

    final_df = my_sql_model_df.selectExpr("*").limit(100)

    return final_df

