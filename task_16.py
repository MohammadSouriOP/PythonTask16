from unittest.mock import patch

import pytest

from task_16 import (get_post_by_id, get_post_by_id_with_validation,
                     get_posts_by_user_id)


@patch('task_16.http_get')
def test_get_post_by_id(mock_get):
    mock_get.return_value.json.return_value = {
         'id': 1, 'title': 'Test Post', 'body': 'Test Body'}
    mock_get.return_value.status_code = 200

    result = get_post_by_id(1)

    assert result == {'id': 1, 'title': 'Test Post', 'body': 'Test Body'}
    mock_get.assert_called_once_with
    ('https://jsonplaceholder.typicode.com/posts/1')


@patch('task_16.http_get')
def test_get_post_by_id_not_found(mock_get):

    mock_get.return_value.status_code = 404
    mock_get.return_value.json.return_value = None

    result = get_post_by_id(999)

    assert result is None


@patch('task_16.http_get')
def test_get_posts_by_user_id(mock_get):
    mock_get.return_value.json.return_value = [{
         'id': 1, 'title': 'Post 1'}, {'id': 2, 'title': 'Post 2'}]
    mock_get.return_value.status_code = 200

    result = get_posts_by_user_id(1)

    assert result == [{
         'id': 1, 'title': 'Post 1'}, {'id': 2, 'title': 'Post 2'}]
    mock_get.assert_called_once_with(
         'https://jsonplaceholder.typicode.com/posts?userId=1')


@patch('task_16.http_get')
def test_get_posts_by_user_id_not_found(mock_get):

    mock_get.return_value.status_code = 404

    mock_get.return_value.json.return_value = None
    result = get_posts_by_user_id(999)

    assert result is None


@patch('task_16.http_get')
def test_get_post_by_id_with_validation(mock_get):

    mock_get.return_value.json.return_value = {
             'id': 1, 'title': 'Test Post', 'body': 'Test Body'}
    mock_get.return_value.status_code = 200
    result = get_post_by_id_with_validation(1)
    assert result == {'id': 1, 'title': 'Test Post', 'body': 'Test Body'}

    with pytest.raises(ValueError, match='post_id must be greater than 0'):
        get_post_by_id_with_validation(0)

    with pytest.raises(ValueError, match='post_id must be greater than 0'):
        get_post_by_id_with_validation(-1)
