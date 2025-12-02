import pytest
import os
from unittest.mock import patch, MagicMock
from core.llm_processor import (
    generate_sql_with_gemini,
    generate_sql_with_claude_code,
    format_schema_for_prompt,
    generate_sql,
    generate_random_query
)
from core.data_models import QueryRequest


class TestLLMProcessor:

    @patch('core.llm_processor.OpenAI')
    def test_generate_sql_with_gemini_success(self, mock_openai_class):
        # Mock OpenAI client (used via Gemini's OpenAI-compatible endpoint)
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client

        mock_response = MagicMock()
        mock_response.choices[0].message.content = "SELECT * FROM users WHERE age > 25"
        mock_client.chat.completions.create.return_value = mock_response

        # Mock environment variable
        with patch.dict(os.environ, {'GEMINI_API_KEY': 'test-gemini-key'}):
            query_text = "Show me users older than 25"
            schema_info = {
                'tables': {
                    'users': {
                        'columns': {'id': 'INTEGER', 'name': 'TEXT', 'age': 'INTEGER'},
                        'row_count': 100
                    }
                }
            }

            result = generate_sql_with_gemini(query_text, schema_info)

            assert result == "SELECT * FROM users WHERE age > 25"
            mock_client.chat.completions.create.assert_called_once()

            # Verify the API call parameters
            call_args = mock_client.chat.completions.create.call_args
            assert call_args[1]['model'] == 'gemini-2.0-flash'
            assert call_args[1]['temperature'] == 0.1
            assert call_args[1]['max_tokens'] == 500

    @patch('core.llm_processor.OpenAI')
    def test_generate_sql_with_gemini_clean_markdown(self, mock_openai_class):
        # Test SQL cleanup from markdown
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client

        mock_response = MagicMock()
        mock_response.choices[0].message.content = "```sql\nSELECT * FROM users\n```"
        mock_client.chat.completions.create.return_value = mock_response

        with patch.dict(os.environ, {'GEMINI_API_KEY': 'test-gemini-key'}):
            query_text = "Show all users"
            schema_info = {'tables': {}}

            result = generate_sql_with_gemini(query_text, schema_info)

            assert result == "SELECT * FROM users"

    def test_generate_sql_with_gemini_no_api_key(self):
        # Test error when API key is not set
        with patch.dict(os.environ, {}, clear=True):
            query_text = "Show all users"
            schema_info = {'tables': {}}

            with pytest.raises(Exception) as exc_info:
                generate_sql_with_gemini(query_text, schema_info)

            assert "GEMINI_API_KEY environment variable not set" in str(exc_info.value)

    @patch('core.llm_processor.OpenAI')
    def test_generate_sql_with_gemini_api_error(self, mock_openai_class):
        # Test API error handling
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client
        mock_client.chat.completions.create.side_effect = Exception("API Error")

        with patch.dict(os.environ, {'GEMINI_API_KEY': 'test-gemini-key'}):
            query_text = "Show all users"
            schema_info = {'tables': {}}

            with pytest.raises(Exception) as exc_info:
                generate_sql_with_gemini(query_text, schema_info)

            assert "Error generating SQL with Gemini" in str(exc_info.value)

    @patch('core.llm_processor.subprocess.run')
    def test_generate_sql_with_claude_code_success(self, mock_subprocess):
        # Mock subprocess for Claude Code CLI
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "SELECT * FROM products WHERE price < 100"
        mock_subprocess.return_value = mock_result

        with patch.dict(os.environ, {'CLAUDE_CODE_PATH': 'claude'}):
            query_text = "Show me products under $100"
            schema_info = {
                'tables': {
                    'products': {
                        'columns': {'id': 'INTEGER', 'name': 'TEXT', 'price': 'REAL'},
                        'row_count': 50
                    }
                }
            }

            result = generate_sql_with_claude_code(query_text, schema_info)

            assert result == "SELECT * FROM products WHERE price < 100"
            mock_subprocess.assert_called_once()

    @patch('core.llm_processor.subprocess.run')
    def test_generate_sql_with_claude_code_clean_markdown(self, mock_subprocess):
        # Test SQL cleanup from markdown
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "```sql\nSELECT * FROM orders\n```"
        mock_subprocess.return_value = mock_result

        with patch.dict(os.environ, {'CLAUDE_CODE_PATH': 'claude'}):
            query_text = "Show all orders"
            schema_info = {'tables': {}}

            result = generate_sql_with_claude_code(query_text, schema_info)

            assert result == "SELECT * FROM orders"

    @patch('core.llm_processor.subprocess.run')
    def test_generate_sql_with_claude_code_error(self, mock_subprocess):
        # Test error handling
        mock_result = MagicMock()
        mock_result.returncode = 1
        mock_result.stderr = "CLI Error"
        mock_subprocess.return_value = mock_result

        with patch.dict(os.environ, {'CLAUDE_CODE_PATH': 'claude'}):
            query_text = "Show all orders"
            schema_info = {'tables': {}}

            with pytest.raises(Exception) as exc_info:
                generate_sql_with_claude_code(query_text, schema_info)

            assert "Claude Code CLI failed" in str(exc_info.value)

    @patch('core.llm_processor.subprocess.run')
    def test_generate_sql_with_claude_code_timeout(self, mock_subprocess):
        # Test timeout handling
        import subprocess
        mock_subprocess.side_effect = subprocess.TimeoutExpired(cmd='claude', timeout=60)

        with patch.dict(os.environ, {'CLAUDE_CODE_PATH': 'claude'}):
            query_text = "Show all orders"
            schema_info = {'tables': {}}

            with pytest.raises(Exception) as exc_info:
                generate_sql_with_claude_code(query_text, schema_info)

            assert "Claude Code CLI timed out" in str(exc_info.value)

    def test_format_schema_for_prompt(self):
        # Test schema formatting for LLM prompt
        schema_info = {
            'tables': {
                'users': {
                    'columns': {'id': 'INTEGER', 'name': 'TEXT', 'age': 'INTEGER'},
                    'row_count': 100
                },
                'products': {
                    'columns': {'id': 'INTEGER', 'name': 'TEXT', 'price': 'REAL'},
                    'row_count': 50
                }
            }
        }

        result = format_schema_for_prompt(schema_info)

        assert "Table: users" in result
        assert "Table: products" in result
        assert "- id (INTEGER)" in result
        assert "- name (TEXT)" in result
        assert "- age (INTEGER)" in result
        assert "- price (REAL)" in result
        assert "Row count: 100" in result
        assert "Row count: 50" in result

    def test_format_schema_for_prompt_empty(self):
        # Test with empty schema
        schema_info = {'tables': {}}

        result = format_schema_for_prompt(schema_info)

        assert result == ""

    @patch('core.llm_processor.generate_sql_with_gemini')
    def test_generate_sql_gemini_priority(self, mock_gemini_func):
        # Test that Gemini is used when GEMINI_API_KEY exists
        mock_gemini_func.return_value = "SELECT * FROM users"

        with patch.dict(os.environ, {'GEMINI_API_KEY': 'gemini-key'}):
            request = QueryRequest(query="Show all users")
            schema_info = {'tables': {}}

            result = generate_sql(request, schema_info)

            assert result == "SELECT * FROM users"
            mock_gemini_func.assert_called_once_with("Show all users", schema_info)

    @patch('core.llm_processor.generate_sql_with_claude_code')
    def test_generate_sql_claude_code_fallback(self, mock_claude_func):
        # Test that Claude Code is used when no Gemini key exists
        mock_claude_func.return_value = "SELECT * FROM products"

        with patch.dict(os.environ, {}, clear=True):
            request = QueryRequest(query="Show all products")
            schema_info = {'tables': {}}

            result = generate_sql(request, schema_info)

            assert result == "SELECT * FROM products"
            mock_claude_func.assert_called_once_with("Show all products", schema_info)

    @patch('core.llm_processor.generate_random_query_with_gemini')
    def test_generate_random_query_gemini_priority(self, mock_gemini_func):
        # Test that Gemini is used for random query when GEMINI_API_KEY exists
        mock_gemini_func.return_value = "What are the top 5 products?"

        with patch.dict(os.environ, {'GEMINI_API_KEY': 'gemini-key'}):
            schema_info = {'tables': {}}

            result = generate_random_query(schema_info)

            assert result == "What are the top 5 products?"
            mock_gemini_func.assert_called_once_with(schema_info)

    @patch('core.llm_processor.generate_random_query_with_claude_code')
    def test_generate_random_query_claude_code_fallback(self, mock_claude_func):
        # Test that Claude Code is used when no Gemini key exists
        mock_claude_func.return_value = "Show me all customers"

        with patch.dict(os.environ, {}, clear=True):
            schema_info = {'tables': {}}

            result = generate_random_query(schema_info)

            assert result == "Show me all customers"
            mock_claude_func.assert_called_once_with(schema_info)
