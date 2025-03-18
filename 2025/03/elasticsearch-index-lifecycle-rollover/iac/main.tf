locals {
  enable_data_streams = true
}

# region thread pool

locals {
  es_thread_pool_alias  = "es-thread-pool"
  es_thread_index_start = "${local.es_thread_pool_alias}-000001"
}

resource "time_sleep" "es_thread_pool_bootstrap_wait_some_seconds" {
  depends_on = [
    elasticstack_elasticsearch_index_template.es_thread_pool,
    elasticstack_elasticsearch_index_lifecycle.es_thread_pool
  ]

  create_duration = "2s"
}

resource "null_resource" "es_thread_pool_bootstrap" {
  count = local.enable_data_streams ? 0 : 1
  provisioner "local-exec" {
    command = <<-EOT
      curl -X PUT \
        -u "${var.elasticsearch_service_account_name}:${var.elasticsearch_service_account_password}" \
        -H "Content-Type: application/json" \
        -d '{"aliases":{"${local.es_thread_pool_alias}":{"is_write_index":true}}}' \
        "${var.elasticsearch_endpoint}/${local.es_thread_index_start}"
    EOT
  }

  depends_on = [
    time_sleep.es_thread_pool_bootstrap_wait_some_seconds
  ]
}

resource "elasticstack_elasticsearch_index_lifecycle" "es_thread_pool" {
  name = "${local.es_thread_pool_alias}-ilm-policy"

  hot {
    min_age = "0ms"
    rollover {
      max_age  = "7d"
      max_size = "5gb"
      max_docs = 2 # To force rollover
    }
    set_priority {
      priority = 100
    }
  }

  warm {
    min_age = "3d"
    set_priority {
      priority = 50
    }
    readonly {}
    forcemerge {
      max_num_segments = 1
    }
    shrink {
      number_of_shards = 1
    }
    allocate {
      require = jsonencode({
        data = "warm"
      })
    }
  }

  cold {
    min_age = "30d"
    set_priority {
      priority = 0
    }
    freeze {}
    allocate {
      require = jsonencode({
        data = "cold"
      })
    }
  }

  delete {
    min_age = "90d"
    delete {
      delete_searchable_snapshot = true
    }
  }
}

# https://www.elastic.co/guide/en/elasticsearch/reference/current/indices-put-template.html
resource "elasticstack_elasticsearch_index_template" "es_thread_pool" {
  name           = "${local.es_thread_pool_alias}-index-template"
  index_patterns = local.enable_data_streams ? [local.es_thread_pool_alias] : ["${local.es_thread_pool_alias}-*"]
  priority       = 50
  dynamic "data_stream" {
    for_each = local.enable_data_streams ? [1] : []
    content {}
  }

  template {
    settings = jsonencode({
      "index.lifecycle.name" : elasticstack_elasticsearch_index_lifecycle.es_thread_pool.name,
      "index.lifecycle.rollover_alias" : local.enable_data_streams ? null : local.es_thread_pool_alias,
      "index.refresh_interval" : "5s",
      # https://www.elastic.co/guide/en/elasticsearch/reference/8.17/index-modules.html#dynamic-index-settings
      "index.number_of_replicas" : 0
    })
    mappings = jsonencode({
      "dynamic" : "strict",
      "_routing" : {
        "required" : false
      },
      "_source" : {
        "enabled" : true
      },
      "properties" : {
        "@timestamp" : {
          "type" : "date"
        },
        "node_name" : {
          "type" : "keyword"
        },
        "name" : {
          "type" : "keyword"
        },
        "active" : {
          "type" : "integer"
        },
        "queue" : {
          "type" : "integer"
        },
        "rejected" : {
          "type" : "integer"
        }
      }
    })
  }
}

resource "elasticstack_kibana_data_view" "es_thread_pool" {
  data_view = {
    name            = "Elasticsearch Thread Pool"
    title           = "${local.es_thread_pool_alias},${local.es_thread_pool_alias}-*"
    time_field_name = "@timestamp"
  }
}

# endregion

# region tasks

locals {
  es_tasks_alias       = "es-tasks"
  es_tasks_index_start = "${local.es_tasks_alias}-000001"
}

resource "time_sleep" "es_tasks_bootstrap_wait_some_seconds" {
  depends_on = [
    elasticstack_elasticsearch_index_template.es_tasks,
    elasticstack_elasticsearch_index_lifecycle.es_tasks
  ]

  create_duration = "2s"
}

resource "null_resource" "es_tasks_bootstrap" {
  count = local.enable_data_streams ? 0 : 1
  provisioner "local-exec" {
    command = <<-EOT
      curl -X PUT \
        -u "${var.elasticsearch_service_account_name}:${var.elasticsearch_service_account_password}" \
        -H "Content-Type: application/json" \
        -d '{"aliases":{"${local.es_tasks_alias}":{"is_write_index":true}}}' \
        "${var.elasticsearch_endpoint}/${local.es_tasks_index_start}"
    EOT
  }

  depends_on = [
    time_sleep.es_tasks_bootstrap_wait_some_seconds
  ]
}

resource "elasticstack_elasticsearch_index_lifecycle" "es_tasks" {
  name = "${local.es_tasks_alias}-ilm-policy"

  hot {
    min_age = "0ms"
    rollover {
      max_age  = "7d"
      max_size = "5gb"
      max_docs = 2 # To force rollover
    }
    set_priority {
      priority = 100
    }
  }

  warm {
    min_age = "3d"
    set_priority {
      priority = 50
    }
    readonly {}
    forcemerge {
      max_num_segments = 1
    }
    shrink {
      number_of_shards = 1
    }
    allocate {
      require = jsonencode({
        data = "warm"
      })
    }
  }

  cold {
    min_age = "30d"
    set_priority {
      priority = 0
    }
    freeze {}
    allocate {
      require = jsonencode({
        data = "cold"
      })
    }
  }
  delete {
    min_age = "90d"
    delete {
      delete_searchable_snapshot = true
    }
  }
}

resource "elasticstack_elasticsearch_index_template" "es_tasks" {
  name           = "${local.es_tasks_alias}-index-template"
  index_patterns = local.enable_data_streams ? [local.es_tasks_alias] : ["${local.es_tasks_alias}-*"]
  priority       = 50
  dynamic "data_stream" {
    for_each = local.enable_data_streams ? [1] : []
    content {}
  }

  template {
    settings = jsonencode({
      "index.lifecycle.name" : elasticstack_elasticsearch_index_lifecycle.es_tasks.name,
      "index.lifecycle.rollover_alias" : local.enable_data_streams ? null : local.es_tasks_alias,
      "index.refresh_interval" : "5s",
      # https://www.elastic.co/guide/en/elasticsearch/reference/8.17/index-modules.html#dynamic-index-settings
      "index.number_of_replicas" : 0
    })
    mappings = jsonencode({
      "dynamic" : "strict",
      "_routing" : {
        "required" : false
      },
      "_source" : {
        "enabled" : true
      },
      "properties" : {
        "@timestamp" : {
          "type" : "date"
        },
        "node" : {
          "type" : "keyword"
        },
        "id" : {
          "type" : "keyword"
        },
        "action" : {
          "type" : "keyword"
        },
        "running_time_milliseconds" : {
          "type" : "long"
        },
        "running_time_string" : {
          "type" : "keyword"
        },
        "cancellable" : {
          "type" : "boolean"
        },
        "parent_task_id" : {
          "type" : "keyword"
        },
        "description" : {
          "type" : "text",
          "fields" : {
            "keyword" : {
              "type" : "keyword",
              "ignore_above" : 256
            }
          }
        }
      }
    })
  }
}

resource "elasticstack_kibana_data_view" "es_tasks" {
  data_view = {
    name            = "Elasticsearch Tasks"
    title           = "${local.es_tasks_alias},${local.es_tasks_alias}-*"
    time_field_name = "@timestamp"
  }
}

# endregion

resource "elasticstack_elasticsearch_security_role" "index_lifecycle_rollover_app" {
  # All cluster privileges are required to perform `GET _cat/thread_pool?v` and `GET /_tasks?pretty=true&human=true&detailed=true`
  cluster = [
    "cluster:monitor/tasks/lists",
    "cluster:monitor/state",
    "cluster:monitor/nodes/info",
    "cluster:monitor/nodes/stats"
  ]
  global = null
  metadata = jsonencode({
    "github"      = "https://github.com/willianantunes/tutorials"
    "environment" = "sandbox"
  })
  name   = "index-lifecycle-rollover-role"
  run_as = []
  indices {
    allow_restricted_indices = false
    names = [
      "${local.es_tasks_alias}-*",
      local.es_tasks_alias,
      "${local.es_thread_pool_alias}-*",
      local.es_thread_pool_alias
    ]
    privileges = ["all"]
    query      = null
    field_security {
      except = []
      grant  = ["*"]
    }
  }
}

resource "elasticstack_elasticsearch_security_user" "index_lifecycle_rollover_app" {
  username  = "index_lifecycle_rollover_20250318"
  password  = "bignosewigblondedguy"
  email     = null
  enabled   = true
  full_name = "ES Index Lifecycle Rollover App"
  metadata = jsonencode({
    "github"      = "https://github.com/willianantunes/tutorials"
    "environment" = "sandbox"
  })
  roles = [
    elasticstack_elasticsearch_security_role.index_lifecycle_rollover_app.name,
  ]
}

resource "elasticstack_elasticsearch_cluster_settings" "cluster_settings" {
  persistent {
    setting {
      name  = "indices.lifecycle.poll_interval"
      value = "1m"
    }
  }
}
