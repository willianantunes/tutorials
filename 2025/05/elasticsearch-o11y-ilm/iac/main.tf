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
      name  = "indices.lifecycle.poll_interval" # To force rollover as fast as possible
      value = "1m"
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

resource "elasticstack_elasticsearch_component_template" "metrics_apm_app_custom" {
  # https://www.elastic.co/docs/reference/fleet/data-streams-scenario1
  name = "metrics-apm.app@custom"

  template {
    settings = jsonencode({
      "index" : {
        "lifecycle" : {
          # This is the default policy. We'll need to create a custom one later.
          "name" : "metrics-apm.app_metrics-default_policy"
          # "name" : elasticstack_elasticsearch_index_lifecycle.metrics_custom_platform.name
        },
        "refresh_interval" : "5s",
        "number_of_shards" : "1",
        "number_of_replicas" : "0"
      }
    })
  }

  metadata = jsonencode(local.tags)
}

# resource "elasticstack_elasticsearch_index_lifecycle" "metrics_custom_platform" {
#   name = "metrics@custom-platform"
#   hot {
#     min_age = "0ms"
#     rollover {
#       max_age                = "30d"
#       max_primary_shard_size = "50gb"
#       max_docs               = 2 # To force rollover
#     }
#   }
#   warm {
#     readonly { enabled = true } # When the rollover is triggered, the index will be set to read-only.
#     migrate { enabled = false }
#   }
#   delete {
#     min_age = "90d"
#     delete {
#       delete_searchable_snapshot = true
#     }
#   }
#   metadata = jsonencode(local.tags)
# }

output "cluster_info" {
  value = data.elasticstack_elasticsearch_info.cluster_info
}
