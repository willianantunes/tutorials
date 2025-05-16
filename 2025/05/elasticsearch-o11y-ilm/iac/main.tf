data "elasticstack_elasticsearch_info" "cluster_info" {}

resource "elasticstack_elasticsearch_cluster_settings" "cluster_settings" {
  transient {
    setting {
      name  = "logger.org.elasticsearch.transport"
      value = "info"
    }
    setting {
      name  = "logger.org.elasticsearch.discovery"
      value = "info"
    }
    setting {
      name  = "logger.org.elasticsearch.cluster"
      value = "info"
    }
  }
  persistent {
    setting {
      name  = "indices.lifecycle.poll_interval"
      value = "10s" # To force rollover as fast as possible
    }
  }
}

resource "elasticstack_elasticsearch_ingest_pipeline" "metrics_apm_app_custom" {
  name        = "metrics-apm.app@custom"
  description = "It's invoked by metrics-apm.app@default-pipeline."

  processors = [
    jsonencode({
      # https://www.elastic.co/docs/reference/enrich-processor/reroute-processor
      "reroute" : {
        "dataset" : [
          "apm.app.all"
        ],
        "if" : "ctx?.data_stream?.dataset != null && ctx.data_stream.dataset.startsWith('apm.app.')"
      }
    })
  ]

  metadata = jsonencode(local.tags)
}

# resource "elasticstack_elasticsearch_component_template" "metrics_apm_app_custom" {
#   # https://www.elastic.co/docs/reference/fleet/data-streams-scenario1
#   name = "metrics-apm.app@custom"
#
#   template {
#     settings = jsonencode({
#       "index" : {
#         "lifecycle" : {
#           # This is the default policy. We'll need to create a custom one later.
#           "name" : "metrics-apm.app_metrics-default_policy"
#           # "name" : elasticstack_elasticsearch_index_lifecycle.metrics_custom_platform.name
#         },
#         "refresh_interval" : "5s",
#         "number_of_shards" : "1",
#         "number_of_replicas" : "0"
#       }
#     })
#   }
#
#   metadata = jsonencode(local.tags)
# }

resource "elasticstack_elasticsearch_component_template" "metrics_custom" {
  name = "metrics@custom"

  template {
    settings = jsonencode({
      "index" : {
        "lifecycle" : {
          "name" : "metrics@lifecycle" # This is the default policy.
          # "name" : elasticstack_elasticsearch_index_lifecycle.all_custom.name
        },
        "refresh_interval" : "5s",
        "number_of_shards" : "1",
        "number_of_replicas" : "0"
      }
    })
  }

  metadata = jsonencode(local.tags)
}

resource "elasticstack_elasticsearch_component_template" "metrics_kubernetes_state_pod_custom" {
  # Check out the data stream `metrics-kubernetes.state_pod-*` and see its component template.
  # After its creation, check out the mapping configuration in the Dev Tools (change the timestamp to yours): GET /.ds-metrics-kubernetes.state_pod-default-2025.06.10-000001/_mapping/field/kubernetes.pod.name
  name = "metrics-kubernetes.state_pod@custom"

  template {
    mappings = jsonencode({
      # https://www.elastic.co/guide/en/elasticsearch/reference/current/properties.html
      properties = {
        # https://www.elastic.co/docs/reference/elasticsearch/mapping-reference/object
        "kubernetes" : {
          "properties" : {
            "pod" : {
              "properties" : {
                "name" : {
                  "type" : "keyword",
                  "ignore_above" : 1024
                  # https://www.elastic.co/docs/reference/elasticsearch/mapping-reference/multi-fields
                  "fields" : {
                    "text" : {
                      "type" : "text"
                    }
                  }
                }
              }
            }
          }
        },
      }
    })
  }

  metadata = jsonencode(local.tags)
}

resource "elasticstack_elasticsearch_component_template" "metrics_kubernetes_pod_custom" {
  provider = elasticstack.o11y
  # Check out the data stream `metrics-kubernetes.pod-*` and see its component template.
  name = "metrics-kubernetes.pod@custom"

  template {
    mappings = jsonencode({
      # https://www.elastic.co/guide/en/elasticsearch/reference/current/properties.html
      properties = {
        # https://www.elastic.co/docs/reference/elasticsearch/mapping-reference/object
        "kubernetes" : {
          "properties" : {
            "pod" : {
              "properties" : {
                "name" : {
                  "type" : "keyword",
                  "ignore_above" : 1024
                  # https://www.elastic.co/docs/reference/elasticsearch/mapping-reference/multi-fields
                  "fields" : {
                    "text" : {
                      "type" : "text"
                    }
                  }
                }
              }
            }
          }
        },
      }
    })
  }

  metadata = jsonencode(local.tags)
}

resource "elasticstack_elasticsearch_component_template" "logs_custom" {
  name = "logs@custom"

  template {
    settings = jsonencode({
      "index" : {
        "lifecycle" : {
          "name" : "logs@lifecycle" # This is the default policy.
          # "name" : elasticstack_elasticsearch_index_lifecycle.all_custom.name
        },
        "refresh_interval" : "5s",
        "number_of_shards" : "1",
        "number_of_replicas" : "0"
      }
    })
  }

  metadata = jsonencode(local.tags)
}

resource "elasticstack_elasticsearch_component_template" "traces_custom" {
  name = "traces@custom"

  template {
    settings = jsonencode({
      "index" : {
        "lifecycle" : {
          "name" : "traces@lifecycle" # This is the default policy.
          # "name" : elasticstack_elasticsearch_index_lifecycle.all_custom.name
        },
        "refresh_interval" : "5s",
        "number_of_shards" : "1",
        "number_of_replicas" : "0"
      }
    })
  }

  metadata = jsonencode(local.tags)
}

resource "elasticstack_elasticsearch_index_lifecycle" "all_custom" {
  name = "all@custom"
  hot {
    min_age = "0ms" # Immediate rollover eligibility
    rollover {
      max_age                = "15d"  # Won't trigger due to max_docs. Just showing the setting.
      max_primary_shard_size = "50gb" # Won't trigger due to max_docs. Just showing the setting.
      max_docs               = 2      # Forces quick rollover to warm
    }
    readonly { enabled = true } # Makes the index read-only after rollover
  }
  warm {
    min_age = "2m" # Minimum age before transitioning to warm phase.
  }
  cold {
    min_age = "4m" # Minimum age before transitioning to cold phase.
  }
  delete {
    min_age = "6m" # Minimum age before deleting the index.
    delete {}      # Permanently deletes the index after the specified age.
  }
}

# resource "elasticstack_elasticsearch_snapshot_lifecycle" "o11y_nightly_snapshots" {
#   name = "o11y-nightly-snapshots"
#
#   schedule      = "0 30 3 * * ?" # Daily at 3:30 AM UTC
#   snapshot_name = "<o11y-nightly-snap-{now/d}>"
#   repository    = "minio" # Manually created. Check out the README.md for details
#
#   indices = [
#     "metrics-*",
#     "logs-*",
#     "traces-*",
#   ]
#   # indices = [
#   #   "<.ds-logs-*-{now-29d}-*>",
#   #   # You can test it in the Dev Tools:
#   #   # - GET /_cat/indices/<.ds-metrics-*-{now-29d}-*>
#   #   # Create the index if you want to test it:
#   #   # - PUT /.ds-metrics-*-{now-29d}-2023.10.01
#   #   "<.ds-metrics-*-{now-29d}-*>",
#   #   "<.ds-traces-*-{now-29d}-*>",
#   # ]
#   ignore_unavailable   = false
#   include_global_state = false
#
#   # `Snapshot retention limits` is crucial to avoid more memory being used on the master node.
#   # We won't configure `expire_after`, `min_count`, and `max_count`, though, for the sake of the learning exercise.
#   # Know more at: https://www.elastic.co/docs/deploy-manage/tools/snapshot-and-restore/create-snapshots#snapshot-retention-limits
# }

output "cluster_info" {
  value = data.elasticstack_elasticsearch_info.cluster_info
}
