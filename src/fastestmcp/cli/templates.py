"""
Templates for FastestMCP CLI
Predefined templates for servers and clients
"""

# Predefined templates
TEMPLATES = {
    'weather': {
        'description': 'Weather app that shows current temperature',
        'tools': ['get_weather', 'get_forecast'],
        'resources': ['weather_data', 'location_info'],
        'prompts': ['weather_summary']
    },
    'file-organizer': {
        'description': 'File organizer that sorts downloads',
        'tools': ['organize_files', 'sort_by_type', 'cleanup_old'],
        'resources': ['file_structure', 'disk_usage'],
        'prompts': ['organization_plan']
    },
    'code-reviewer': {
        'description': 'Code reviewer that checks for bugs',
        'tools': ['review_code', 'check_bugs', 'suggest_fixes'],
        'resources': ['code_analysis', 'bug_reports'],
        'prompts': ['review_summary']
    },
    'github-monitor': {
        'description': 'GitHub repo monitor',
        'tools': ['monitor_repo', 'get_issues', 'check_prs'],
        'resources': ['repo_data', 'contributor_stats'],
        'prompts': ['repo_health_report']
    },
    'todo-manager': {
        'description': 'Todo list manager',
        'tools': ['add_todo', 'list_todos', 'complete_todo', 'delete_todo'],
        'resources': ['todo_list', 'completed_tasks'],
        'prompts': ['productivity_report']
    },
    'subscription-server': {
        'description': 'MCP server with subscription-based notifications',
        'tools': ['broadcast_notification', 'manage_subscriptions', 'send_event'],
        'resources': ['subscription_list', 'notification_history', 'event_log'],
        'prompts': ['subscription_help', 'notification_guide'],
        'notifications': ['status_update', 'system_alert', 'user_notification'],
        'subscriptions': ['event_stream', 'data_feed', 'status_monitor']
    },
    'event-driven-server': {
        'description': 'Event-driven MCP server with real-time notifications',
        'tools': ['trigger_event', 'broadcast_update', 'handle_subscription'],
        'resources': ['event_stream', 'notification_queue', 'subscriber_list'],
        'prompts': ['event_handling_guide', 'subscription_management'],
        'notifications': ['event_triggered', 'system_status', 'data_update'],
        'subscriptions': ['realtime_events', 'status_changes', 'data_stream']
    }
}

# Client templates for MCP clients
CLIENT_TEMPLATES = {
    'api-client': {
        'description': 'Generic API client for REST/GraphQL services',
        'apis': ['rest_api', 'graphql_api', 'webhook_handler'],
        'integrations': ['http_client', 'auth_handler', 'rate_limiter'],
        'handlers': ['request_processor', 'response_parser']
    },
    'database-client': {
        'description': 'Database client for SQL/NoSQL databases',
        'apis': ['query_executor', 'schema_inspector', 'migration_runner'],
        'integrations': ['connection_pool', 'query_builder', 'result_formatter'],
        'handlers': ['transaction_manager', 'error_handler']
    },
    'filesystem-client': {
        'description': 'File system client for file operations',
        'apis': ['file_manager', 'directory_scanner', 'permission_handler'],
        'integrations': ['path_resolver', 'file_watcher', 'sync_manager'],
        'handlers': ['io_processor', 'metadata_extractor']
    },
    'notification-client': {
        'description': 'MCP client with subscription-based notifications',
        'apis': ['notification_api', 'subscription_api', 'event_handler'],
        'integrations': ['priority_queue', 'event_processor', 'notification_filter'],
        'handlers': ['notification_handler', 'subscription_manager'],
        'notifications': ['priority_notifications', 'system_alerts', 'user_messages'],
        'subscriptions': ['event_feed', 'status_updates', 'data_stream']
    },
    'monitoring-client': {
        'description': 'System monitoring and metrics client',
        'apis': ['metrics_collector', 'alert_manager', 'log_aggregator'],
        'integrations': ['time_series_db', 'alert_rules', 'dashboard_generator'],
        'handlers': ['data_processor', 'threshold_checker'],
        'notifications': ['alert_notifications', 'metric_alerts', 'system_warnings'],
        'subscriptions': ['metrics_stream', 'log_feed', 'alert_stream']
    }
}