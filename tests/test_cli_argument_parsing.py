import pytest
import sys
import os
from unittest.mock import patch, MagicMock
from pathlib import Path
import argparse


class TestCLIArgumentParsing:
    """Test CLI argument parsing functionality"""

    @patch('fastestmcp.cli.__main__.generate_level_boilerplate')
    @patch('fastestmcp.cli.__main__.generate_complex_server')
    def test_parse_new_level_args(self, mock_generate_complex, mock_generate_level):
        """Test parsing new command with level arguments"""
        from fastestmcp.cli.__main__ import main

        test_args = ['new', '--level', '3', '--name', 'test_server']
        with patch('sys.argv', ['fastestmcp'] + test_args):
            main()

        mock_generate_level.assert_called_once_with(3, 'test_server', '.')

    @patch('fastestmcp.cli.__main__.generate_server_from_template')
    def test_parse_new_template_args(self, mock_generate_template):
        """Test parsing new command with template arguments"""
        from fastestmcp.cli.__main__ import main

        test_args = ['new', '--template', 'weather', '--name', 'weather_app']
        with patch('sys.argv', ['fastestmcp'] + test_args):
            main()

        mock_generate_template.assert_called_once_with('weather', 'weather_app', '.')

    @patch('fastestmcp.cli.__main__.generate_complex_server')
    def test_parse_new_custom_args(self, mock_generate_complex):
        """Test parsing new command with custom arguments"""
        mock_generate_complex.return_value = ("Server generated successfully", "folder structure")
        from fastestmcp.cli.__main__ import main

        test_args = [
            'new', '--name', 'custom_server',
            '--tools', '5', '--resources', '3', '--prompts', '2',
            '--notifications', '3', '--subscriptions', '2',
            '--transport', 'http', '--structure', 'structured',
            '--type', 'fastmcp', '--output', '/tmp'
        ]
        with patch('sys.argv', ['fastestmcp'] + test_args):
            main()

        mock_generate_complex.assert_called_once_with(
            name='custom_server',
            tools=5,
            resources=3,
            prompts=2,
            notifications=3,
            subscriptions=2,
            transport='http',
            structure='structured',
            server_type='fastmcp',
            output_dir='/tmp'
        )

    @patch('fastestmcp.cli.__main__.generate_complex_client')
    def test_parse_client_custom_args(self, mock_generate_client):
        """Test parsing client command with custom arguments"""
        mock_generate_client.return_value = ("Client generated successfully", "folder structure")
        from fastestmcp.cli.__main__ import main

        test_args = [
            'client', '--name', 'test_client',
            '--apis', '3', '--integrations', '2', '--handlers', '1',
            '--notifications', '2', '--subscriptions', '1',
            '--transport', 'http', '--structure', 'structured',
            '--type', 'fastmcp', '--output', '/tmp'
        ]
        with patch('sys.argv', ['fastestmcp'] + test_args):
            main()

        mock_generate_client.assert_called_once_with(
            name='test_client',
            apis=3,
            integrations=2,
            handlers=1,
            notifications=2,
            subscriptions=1,
            transport='http',
            structure='structured',
            client_type='fastmcp',
            output_dir='/tmp'
        )

    @patch('fastestmcp.cli.__main__.generate_complex_client')
    def test_parse_client_template_args(self, mock_generate_client):
        """Test parsing client command with template arguments"""
        mock_generate_client.return_value = ("Client generated successfully", "folder structure")
        from fastestmcp.cli.__main__ import main

        # Mock CLIENT_TEMPLATES to include a test template
        with patch('fastestmcp.cli.__main__.CLIENT_TEMPLATES', {
            'api-client': {'apis': ['endpoint1'], 'integrations': ['int1'], 'handlers': ['handler1']},
            'notification-client': {
                'apis': ['notification_api', 'subscription_api', 'event_handler'],
                'integrations': ['priority_queue', 'event_processor', 'notification_filter'],
                'handlers': ['notification_handler', 'subscription_manager'],
                'notifications': ['priority_notifications', 'system_alerts', 'user_messages'],
                'subscriptions': ['event_feed', 'status_updates', 'data_stream']
            }
        }):
            test_args = ['client', '--template', 'notification-client', '--name', 'notification_client']
            with patch('sys.argv', ['fastestmcp'] + test_args):
                main()

        mock_generate_client.assert_called_once_with(
            name='notification_client',
            apis=3,  # len of template apis
            integrations=3,  # len of template integrations
            handlers=2,  # len of template handlers
            notifications=3,  # len of template notifications
            subscriptions=3,  # len of template subscriptions
            transport='stdio',
            structure='mono',
            client_type='fastmcp',
            output_dir='.'
        )

    def test_default_values_server(self):
        """Test default values for server generation"""
        from fastestmcp.cli.__main__ import main

        with patch('fastestmcp.cli.__main__.generate_complex_server') as mock_generate:
            mock_generate.return_value = ("Server generated successfully", "folder structure")
            test_args = ['new', '--name', 'default_server']
            with patch('sys.argv', ['fastestmcp'] + test_args):
                main()

        # Check that defaults are used
        call_args = mock_generate.call_args[1]
        assert call_args['tools'] == 2
        assert call_args['resources'] == 1
        assert call_args['prompts'] == 0
        assert call_args['notifications'] == 0
        assert call_args['subscriptions'] == 0
        assert call_args['transport'] == 'stdio'
        assert call_args['structure'] == 'mono'
        assert call_args['server_type'] == 'fastmcp'
        assert call_args['output_dir'] == '.'

    def test_default_values_client(self):
        """Test default values for client generation"""
        from fastestmcp.cli.__main__ import main

        with patch('fastestmcp.cli.__main__.generate_complex_client') as mock_generate:
            mock_generate.return_value = ("Client generated successfully", "folder structure")
            test_args = ['client', '--name', 'default_client']
            with patch('sys.argv', ['fastestmcp'] + test_args):
                main()

        # Check that defaults are used
        call_args = mock_generate.call_args[1]
        assert call_args['apis'] == 2
        assert call_args['integrations'] == 1
        assert call_args['handlers'] == 1
        assert call_args['notifications'] == 0
        assert call_args['subscriptions'] == 0
        assert call_args['transport'] == 'stdio'
        assert call_args['structure'] == 'mono'
        assert call_args['client_type'] == 'fastmcp'
        assert call_args['output_dir'] == '.'

    def test_invalid_level_choice(self):
        """Test that invalid level raises SystemExit"""
        from fastestmcp.cli.__main__ import main

        test_args = ['new', '--level', '10', '--name', 'test']
        with patch('sys.argv', ['fastestmcp'] + test_args):
            with pytest.raises(SystemExit):
                main()

    def test_invalid_template_choice(self):
        """Test that invalid template raises SystemExit"""
        from fastestmcp.cli.__main__ import main

        test_args = ['new', '--template', 'nonexistent', '--name', 'test']
        with patch('sys.argv', ['fastestmcp'] + test_args):
            with pytest.raises(SystemExit):
                main()

    def test_invalid_transport_choice_server(self):
        """Test that invalid transport for server raises SystemExit"""
        from fastestmcp.cli.__main__ import main

        test_args = ['new', '--name', 'test', '--transport', 'invalid']
        with patch('sys.argv', ['fastestmcp'] + test_args):
            with pytest.raises(SystemExit):
                main()

    def test_invalid_transport_choice_client(self):
        """Test that invalid transport for client raises SystemExit"""
        from fastestmcp.cli.__main__ import main

        test_args = ['client', '--name', 'test', '--transport', 'invalid']
        with patch('sys.argv', ['fastestmcp'] + test_args):
            with pytest.raises(SystemExit):
                main()

    def test_invalid_structure_choice(self):
        """Test that invalid structure raises SystemExit"""
        from fastestmcp.cli.__main__ import main

        test_args = ['new', '--name', 'test', '--structure', 'invalid']
        with patch('sys.argv', ['fastestmcp'] + test_args):
            with pytest.raises(SystemExit):
                main()

    def test_invalid_type_choice_server(self):
        """Test that invalid type for server raises SystemExit"""
        from fastestmcp.cli.__main__ import main

        test_args = ['new', '--name', 'test', '--type', 'invalid']
        with patch('sys.argv', ['fastestmcp'] + test_args):
            with pytest.raises(SystemExit):
                main()

    def test_invalid_type_choice_client(self):
        """Test that invalid type for client raises SystemExit"""
        from fastestmcp.cli.__main__ import main

        test_args = ['client', '--name', 'test', '--type', 'invalid']
        with patch('sys.argv', ['fastestmcp'] + test_args):
            with pytest.raises(SystemExit):
                main()

    def test_missing_required_name_server(self):
        """Test that missing name for server raises SystemExit"""
        from fastestmcp.cli.__main__ import main

        test_args = ['new', '--level', '1']
        with patch('sys.argv', ['fastestmcp'] + test_args):
            with pytest.raises(SystemExit):
                main()

    def test_missing_required_name_client(self):
        """Test that missing name for client raises SystemExit"""
        from fastestmcp.cli.__main__ import main

        test_args = ['client', '--apis', '2']
        with patch('sys.argv', ['fastestmcp'] + test_args):
            with pytest.raises(SystemExit):
                main()

    def test_help_flag_server(self):
        """Test that --help flag works for server command"""
        from fastestmcp.cli.__main__ import main

        test_args = ['new', '--help']
        with patch('sys.argv', ['fastestmcp'] + test_args):
            with pytest.raises(SystemExit):
                main()

    def test_help_flag_client(self):
        """Test that --help flag works for client command"""
        from fastestmcp.cli.__main__ import main

        test_args = ['client', '--help']
        with patch('sys.argv', ['fastestmcp'] + test_args):
            with pytest.raises(SystemExit):
                main()

    def test_main_help_flag(self):
        """Test that main --help flag works"""
        from fastestmcp.cli.__main__ import main

        test_args = ['--help']
        with patch('sys.argv', ['fastestmcp'] + test_args):
            with pytest.raises(SystemExit):
                main()

    @patch('fastestmcp.cli.__main__.generate_complex_server')
    def test_parse_new_with_notifications_subscriptions(self, mock_generate_complex):
        """Test parsing new command with notification and subscription parameters"""
        mock_generate_complex.return_value = ("Server generated successfully", "folder structure")
        from fastestmcp.cli.__main__ import main

        test_args = [
            'new', '--name', 'notification_server',
            '--notifications', '5', '--subscriptions', '3'
        ]
        with patch('sys.argv', ['fastestmcp'] + test_args):
            main()

        mock_generate_complex.assert_called_once_with(
            name='notification_server',
            tools=2,
            resources=1,
            prompts=0,
            notifications=5,
            subscriptions=3,
            transport='stdio',
            structure='mono',
            server_type='fastmcp',
            output_dir='.'
        )

    @patch('fastestmcp.cli.__main__.generate_complex_client')
    def test_parse_client_with_notifications_subscriptions(self, mock_generate_client):
        """Test parsing client command with notification and subscription parameters"""
        mock_generate_client.return_value = ("Client generated successfully", "folder structure")
        from fastestmcp.cli.__main__ import main

        test_args = [
            'client', '--name', 'notification_client',
            '--notifications', '4', '--subscriptions', '2'
        ]
        with patch('sys.argv', ['fastestmcp'] + test_args):
            main()

        mock_generate_client.assert_called_once_with(
            name='notification_client',
            apis=2,
            integrations=1,
            handlers=1,
            notifications=4,
            subscriptions=2,
            transport='stdio',
            structure='mono',
            client_type='fastmcp',
            output_dir='.'
        )