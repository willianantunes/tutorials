terraform {
  required_providers {
    elasticstack = {
      source  = "elastic/elasticstack"
      version = "0.11.6"
    }
    env = {
      source  = "tcarreira/env"
      version = "0.2.0"
    }
  }
}

locals {
  envs = { for tuple in regexall("(.*)=(.*)", file(".env")) : tuple[0] => tuple[1] }
}

provider "elasticstack" {
  kibana {
    username  = local.envs["ELASTIC_USERNAME"]
    password  = local.envs["ELASTIC_PASSWORD"]
    endpoints = ["https://localhost:${local.envs["KIBANA_PORT"]}"]
    insecure  = true
  }
  elasticsearch {
    username  = local.envs["ELASTIC_USERNAME"]
    password  = local.envs["ELASTIC_PASSWORD"]
    endpoints = ["https://localhost:${local.envs["ELASTICSEARCH_PORT"]}"]
    insecure  = true
  }
}

resource "elasticstack_fleet_integration" "k8s" {
  name    = "kubernetes"
  version = "1.66.2"
}

resource "elasticstack_fleet_agent_policy" "k8s_kind" {
  name            = "K8S Kind Agent Policy"
  namespace       = "development"
  monitor_logs    = true
  monitor_metrics = true
  sys_monitoring  = true
}

resource "elasticstack_fleet_integration_policy" "k8s_kind" {
  name                = "K8S Kind Integration Policy"
  namespace           = "development"
  agent_policy_id     = elasticstack_fleet_agent_policy.k8s_kind.policy_id
  integration_name    = elasticstack_fleet_integration.k8s.name
  integration_version = elasticstack_fleet_integration.k8s.version

  input {
    input_id = "kubelet-kubernetes/metrics"
    streams_json = jsonencode({
      "kubernetes.container" : {
        "enabled" : true,
        "vars" : {
          "add_metadata" : true,
          "add_resource_metadata_config" : "# add_resource_metadata:\n#   namespace:\n#     include_labels: [\"namespacelabel1\"]\n#   node:\n#     include_labels: [\"nodelabel2\"]\n#     include_annotations: [\"nodeannotation1\"]\n#   deployment: false\n",
          "bearer_token_file" : "/var/run/secrets/kubernetes.io/serviceaccount/token",
          "hosts" : [
            "https://$${env.NODE_NAME}:10250"
          ],
          "period" : "10s",
          "ssl.certificate_authorities" : [],
          "ssl.verification_mode" : "none"
        }
      },
      "kubernetes.node" : {
        "enabled" : true,
        "vars" : {
          "add_metadata" : true,
          "bearer_token_file" : "/var/run/secrets/kubernetes.io/serviceaccount/token",
          "hosts" : [
            "https://$${env.NODE_NAME}:10250"
          ],
          "period" : "10s",
          "ssl.certificate_authorities" : [],
          "ssl.verification_mode" : "none"
        }
      },
      "kubernetes.pod" : {
        "enabled" : true,
        "vars" : {
          "add_metadata" : true,
          "add_resource_metadata_config" : "# add_resource_metadata:\n#   namespace:\n#     include_labels: [\"namespacelabel1\"]\n#   node:\n#     include_labels: [\"nodelabel2\"]\n#     include_annotations: [\"nodeannotation1\"]\n#   deployment: false\n",
          "bearer_token_file" : "/var/run/secrets/kubernetes.io/serviceaccount/token",
          "hosts" : [
            "https://$${env.NODE_NAME}:10250"
          ],
          "period" : "10s",
          "ssl.certificate_authorities" : [],
          "ssl.verification_mode" : "none"
        }
      },
      "kubernetes.system" : {
        "enabled" : true,
        "vars" : {
          "add_metadata" : true,
          "bearer_token_file" : "/var/run/secrets/kubernetes.io/serviceaccount/token",
          "hosts" : [
            "https://$${env.NODE_NAME}:10250"
          ],
          "period" : "10s",
          "ssl.certificate_authorities" : [],
          "ssl.verification_mode" : "none"
        }
      },
      "kubernetes.volume" : {
        "enabled" : true,
        "vars" : {
          "add_metadata" : true,
          "bearer_token_file" : "/var/run/secrets/kubernetes.io/serviceaccount/token",
          "hosts" : [
            "https://$${env.NODE_NAME}:10250"
          ],
          "period" : "10s",
          "ssl.certificate_authorities" : [],
          "ssl.verification_mode" : "none"
        }
      }
    })
  }

  input {
    input_id = "kube-state-metrics-kubernetes/metrics"
    streams_json = jsonencode({
      "kubernetes.state_container" : {
        "enabled" : true,
        "vars" : {
          "add_metadata" : true,
          "add_resource_metadata_config" : "# add_resource_metadata:\n#   namespace:\n#     include_labels: [\"namespacelabel1\"]\n#   node:\n#     include_labels: [\"nodelabel2\"]\n#     include_annotations: [\"nodeannotation1\"]\n#   deployment: false\n",
          "bearer_token_file" : "/var/run/secrets/kubernetes.io/serviceaccount/token",
          "hosts" : [
            "kube-state-metrics:8080"
          ],
          "leaderelection" : true,
          "period" : "10s",
          "ssl.certificate_authorities" : []
        }
      },
      "kubernetes.state_cronjob" : {
        "enabled" : true,
        "vars" : {
          "add_metadata" : true,
          "bearer_token_file" : "/var/run/secrets/kubernetes.io/serviceaccount/token",
          "hosts" : [
            "kube-state-metrics:8080"
          ],
          "leaderelection" : true,
          "period" : "10s",
          "ssl.certificate_authorities" : []
        }
      },
      "kubernetes.state_daemonset" : {
        "enabled" : true,
        "vars" : {
          "add_metadata" : true,
          "bearer_token_file" : "/var/run/secrets/kubernetes.io/serviceaccount/token",
          "hosts" : [
            "kube-state-metrics:8080"
          ],
          "leaderelection" : true,
          "period" : "10s",
          "ssl.certificate_authorities" : []
        }
      },
      "kubernetes.state_deployment" : {
        "enabled" : true,
        "vars" : {
          "add_metadata" : true,
          "bearer_token_file" : "/var/run/secrets/kubernetes.io/serviceaccount/token",
          "hosts" : [
            "kube-state-metrics:8080"
          ],
          "leaderelection" : true,
          "period" : "10s",
          "ssl.certificate_authorities" : []
        }
      },
      "kubernetes.state_job" : {
        "enabled" : true,
        "vars" : {
          "add_metadata" : true,
          "bearer_token_file" : "/var/run/secrets/kubernetes.io/serviceaccount/token",
          "hosts" : [
            "kube-state-metrics:8080"
          ],
          "leaderelection" : true,
          "period" : "10s",
          "ssl.certificate_authorities" : []
        }
      },
      "kubernetes.state_namespace" : {
        "enabled" : true,
        "vars" : {
          "add_metadata" : true,
          "bearer_token_file" : "/var/run/secrets/kubernetes.io/serviceaccount/token",
          "hosts" : [
            "kube-state-metrics:8080"
          ],
          "leaderelection" : true,
          "period" : "10s",
          "ssl.certificate_authorities" : []
        }
      },
      "kubernetes.state_node" : {
        "enabled" : true,
        "vars" : {
          "add_metadata" : true,
          "bearer_token_file" : "/var/run/secrets/kubernetes.io/serviceaccount/token",
          "hosts" : [
            "kube-state-metrics:8080"
          ],
          "leaderelection" : true,
          "period" : "10s",
          "ssl.certificate_authorities" : []
        }
      },
      "kubernetes.state_persistentvolume" : {
        "enabled" : true,
        "vars" : {
          "add_metadata" : true,
          "bearer_token_file" : "/var/run/secrets/kubernetes.io/serviceaccount/token",
          "hosts" : [
            "kube-state-metrics:8080"
          ],
          "leaderelection" : true,
          "period" : "10s",
          "ssl.certificate_authorities" : []
        }
      },
      "kubernetes.state_persistentvolumeclaim" : {
        "enabled" : true,
        "vars" : {
          "add_metadata" : true,
          "bearer_token_file" : "/var/run/secrets/kubernetes.io/serviceaccount/token",
          "hosts" : [
            "kube-state-metrics:8080"
          ],
          "leaderelection" : true,
          "period" : "10s",
          "ssl.certificate_authorities" : []
        }
      },
      "kubernetes.state_pod" : {
        "enabled" : true,
        "vars" : {
          "add_metadata" : true,
          "add_resource_metadata_config" : "# add_resource_metadata:\n#   namespace:\n#     include_labels: [\"namespacelabel1\"]\n#   node:\n#     include_labels: [\"nodelabel2\"]\n#     include_annotations: [\"nodeannotation1\"]\n#   deployment: false\n",
          "bearer_token_file" : "/var/run/secrets/kubernetes.io/serviceaccount/token",
          "hosts" : [
            "kube-state-metrics:8080"
          ],
          "leaderelection" : true,
          "period" : "10s",
          "ssl.certificate_authorities" : []
        }
      },
      "kubernetes.state_replicaset" : {
        "enabled" : true,
        "vars" : {
          "add_metadata" : true,
          "bearer_token_file" : "/var/run/secrets/kubernetes.io/serviceaccount/token",
          "hosts" : [
            "kube-state-metrics:8080"
          ],
          "leaderelection" : true,
          "period" : "10s",
          "ssl.certificate_authorities" : []
        }
      },
      "kubernetes.state_resourcequota" : {
        "enabled" : true,
        "vars" : {
          "add_metadata" : true,
          "bearer_token_file" : "/var/run/secrets/kubernetes.io/serviceaccount/token",
          "hosts" : [
            "kube-state-metrics:8080"
          ],
          "leaderelection" : true,
          "period" : "10s",
          "ssl.certificate_authorities" : []
        }
      },
      "kubernetes.state_service" : {
        "enabled" : true,
        "vars" : {
          "add_metadata" : true,
          "bearer_token_file" : "/var/run/secrets/kubernetes.io/serviceaccount/token",
          "hosts" : [
            "kube-state-metrics:8080"
          ],
          "leaderelection" : true,
          "period" : "10s",
          "ssl.certificate_authorities" : []
        }
      },
      "kubernetes.state_statefulset" : {
        "enabled" : true,
        "vars" : {
          "add_metadata" : true,
          "bearer_token_file" : "/var/run/secrets/kubernetes.io/serviceaccount/token",
          "hosts" : [
            "kube-state-metrics:8080"
          ],
          "leaderelection" : true,
          "period" : "10s",
          "ssl.certificate_authorities" : []
        }
      },
      "kubernetes.state_storageclass" : {
        "enabled" : true,
        "vars" : {
          "add_metadata" : true,
          "bearer_token_file" : "/var/run/secrets/kubernetes.io/serviceaccount/token",
          "hosts" : [
            "kube-state-metrics:8080"
          ],
          "leaderelection" : true,
          "period" : "10s",
          "ssl.certificate_authorities" : []
        }
      }
    })
  }

  input {
    input_id = "kube-proxy-kubernetes/metrics"
    streams_json = jsonencode({
      "kubernetes.proxy" : {
        "enabled" : true,
        "vars" : {
          "hosts" : [
            "localhost:10249"
          ],
          "period" : "10s"
        }
      }
    })
  }

  input {
    input_id = "container-logs-filestream"
    streams_json = jsonencode({
      "kubernetes.container_logs" : {
        "enabled" : true,
        "vars" : {
          "additionalParsersConfig" : "# - ndjson:\n#     target: json\n#     ignore_decoding_error: true\n# - multiline:\n#     type: pattern\n#     pattern: '^\\['\n#     negate: true\n#     match: after\n",
          "containerParserFormat" : "auto",
          "containerParserStream" : "all",
          "custom" : "",
          "data_stream.dataset" : "kubernetes.container_logs",
          "paths" : [
            "/var/log/containers/*$${kubernetes.container.id}.log"
          ],
          "symlinks" : true
        }
      }
    })
  }

  input {
    input_id = "kube-apiserver-kubernetes/metrics"
    streams_json = jsonencode({
      "kubernetes.apiserver" : {
        "enabled" : true,
        "vars" : {
          "bearer_token_file" : "/var/run/secrets/kubernetes.io/serviceaccount/token",
          "hosts" : [
            "https://$${env.KUBERNETES_SERVICE_HOST}:$${env.KUBERNETES_SERVICE_PORT}"
          ],
          "leaderelection" : true,
          "period" : "30s",
          "ssl.certificate_authorities" : [
            "/var/run/secrets/kubernetes.io/serviceaccount/ca.crt"
          ]
        }
      }
    })
  }

  input {
    input_id = "kube-scheduler-kubernetes/metrics"
    streams_json = jsonencode({
      "kubernetes.scheduler" : {
        "enabled" : true,
        "vars" : {
          "bearer_token_file" : "/var/run/secrets/kubernetes.io/serviceaccount/token",
          "hosts" : [
            "https://0.0.0.0:10259"
          ],
          "period" : "10s",
          "scheduler_label_key" : "component",
          "scheduler_label_value" : "kube-scheduler",
          "ssl.verification_mode" : "none"
        }
      }
    })
  }

  input {
    input_id = "kube-controller-manager-kubernetes/metrics"
    streams_json = jsonencode({
      "kubernetes.controllermanager" : {
        "enabled" : true,
        "vars" : {
          "bearer_token_file" : "/var/run/secrets/kubernetes.io/serviceaccount/token",
          "controller_manager_label_key" : "component",
          "controller_manager_label_value" : "kube-controller-manager",
          "hosts" : [
            "https://0.0.0.0:10257"
          ],
          "period" : "10s",
          "ssl.verification_mode" : "none"
        }
      }
    })
  }

  input {
    input_id = "events-kubernetes/metrics"
    streams_json = jsonencode({
      "kubernetes.event" : {
        "enabled" : true,
        "vars" : {
          "add_metadata" : true,
          "leaderelection" : true,
          "period" : "10s",
          "skip_older" : true
        }
      }
    })
  }

  input {
    input_id = "audit-logs-filestream"
    streams_json = jsonencode({
      "kubernetes.audit_logs" : {
        "enabled" : true,
        "vars" : {
          "paths" : [
            "/var/log/kubernetes/kube-apiserver-audit.log"
          ]
        }
      }
    })
  }
}

resource "elasticstack_elasticsearch_security_api_key" "k8s_kind" {
  name = "K8S Kind API Key"
  # https://www.elastic.co/guide/en/fleet/8.15/grant-access-to-elasticsearch.html#create-api-key-standalone-agent
  role_descriptors = jsonencode({
    "standalone_agent" : {
      "cluster" : [
        "monitor"
      ],
      "indices" : [
        {
          "names" : [
            "logs-*-*",
            "metrics-*-*",
            "traces-*-*",
            "synthetics-*-*"
          ],
          "privileges" : [
            "auto_configure",
            "create_doc"
          ],
          "allow_restricted_indices" : false
        }
      ],
      "applications" : [],
      "run_as" : [],
      "metadata" : {},
      "transient_metadata" : {
        "enabled" : true
      }
    }
  })
  metadata = jsonencode({
    "env"              = "development"
    "terraformManaged" = true
  })
}

output "api_key_k8s_kind" {
  value     = elasticstack_elasticsearch_security_api_key.k8s_kind
  sensitive = true
}
