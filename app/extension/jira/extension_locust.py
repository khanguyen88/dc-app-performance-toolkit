from locustio.common_utils import raise_if_login_failed, fetch_by_re, RESOURCE_HEADERS, timestamp_int, \
    generate_random_string, TEXT_HEADERS, init_logger, jira_measure
from locustio.jira.requests_params import EditIssue, AddComment

logger = init_logger(app_type='jira')


def app_specific_action(locust):
    edit_issue_to_trigger_outbound_notification(locust)
    add_comment_trigger_outbound_notification(locust)


@jira_measure("locust_edit_issue_to_trigger_outbound_notification")
def edit_issue_to_trigger_outbound_notification(locust):
    params = EditIssue()
    issue_id = 2013911
    issue_key = "DEV-5"
    project_key = "DEV"

    @jira_measure('locust_edit_issue_to_trigger_outbound_notification:open_editor')
    def edit_issue_open_editor():
        raise_if_login_failed(locust)
        r = locust.get(f'/secure/EditIssue!default.jspa?id={issue_id}', catch_response=True)
        content = r.content.decode('utf-8')

        issue_type = fetch_by_re(params.issue_type_pattern, content)
        atl_token = fetch_by_re(params.atl_token_pattern, content)
        priority = fetch_by_re(params.issue_priority_pattern, content, group_no=2)
        assignee = fetch_by_re(params.issue_assigneee_reporter_pattern, content, group_no=2)
        reporter = fetch_by_re(params.issue_reporter_pattern, content)

        if not (f' Edit Issue:  [{issue_key}]' in content):
            logger.error(f'{params.err_message_issue_not_found} - {issue_id}, {issue_key}: {content}')
        assert f' Edit Issue:  [{issue_key}]' in content, \
            params.err_message_issue_not_found
        logger.locust_info(f"{params.action_name}: Editing issue {issue_key}")

        locust.post('/rest/webResources/1.0/resources', json=params.resources_body.get("705"),
                    headers=RESOURCE_HEADERS, catch_response=True)
        locust.post('/rest/webResources/1.0/resources', json=params.resources_body.get("710"),
                    headers=RESOURCE_HEADERS, catch_response=True)
        locust.post('/rest/webResources/1.0/resources', json=params.resources_body.get("720"),
                    headers=RESOURCE_HEADERS, catch_response=True)
        locust.get(f'/rest/internal/2/user/mention/search?issueKey={issue_key}'
                   f'&projectKey={project_key}&maxResults=10&_={timestamp_int()}', catch_response=True)

        edit_body = f'id={issue_id}&summary="DC-TestIssue{generate_random_string(15)}"&issueType={issue_type}&priority={priority}' \
                    f'&dueDate=""&assignee={assignee}&reporter={reporter}&environment=""' \
                    f'&description={generate_random_string(500)}&timetracking_originalestimate=""' \
                    f'&timetracking_remainingestimate=""&isCreateIssue=""&hasWorkStarted=""&dnd-dropzone=""' \
                    f'&comment=""&commentLevel=""&atl_token={atl_token}&Update=Update'
        locust.session_data_storage['edit_issue_body'] = edit_body
        locust.session_data_storage['atl_token'] = atl_token

    edit_issue_open_editor()

    @jira_measure('locust_edit_issue_to_trigger_outbound_notification:save_edit')
    def edit_issue_save_edit():
        raise_if_login_failed(locust)
        r = locust.post(f'/secure/EditIssue.jspa?atl_token={locust.session_data_storage["atl_token"]}',
                        params=locust.session_data_storage['edit_issue_body'],
                        headers=TEXT_HEADERS, catch_response=True)
        content = r.content.decode('utf-8')
        if not (f'[{issue_key}]' in content):
            logger.error(f'Could not save edited page: {content}')
        assert f'[{issue_key}]' in content, 'Could not save edited page'

        locust.get(f'/browse/{issue_key}', catch_response=True)
        locust.post('/rest/webResources/1.0/resources', json=params.resources_body.get("740"),
                    headers=RESOURCE_HEADERS, catch_response=True)
        locust.post('/rest/webResources/1.0/resources', json=params.resources_body.get("745"),
                    headers=RESOURCE_HEADERS, catch_response=True)
        locust.post('/rest/webResources/1.0/resources', json=params.resources_body.get("765"),
                    headers=RESOURCE_HEADERS, catch_response=True)
        locust.get(f'/secure/AjaxIssueEditAction!default.jspa?decorator=none&issueId='
                   f'{issue_id}&_={timestamp_int()}', catch_response=True)
        locust.post('/rest/webResources/1.0/resources', json=params.resources_body.get("775"),
                    headers=RESOURCE_HEADERS, catch_response=True)
        locust.client.put(f'/rest/projects/1.0/project/{project_key}/lastVisited', params.last_visited_body,
                          catch_response=True)

    edit_issue_save_edit()


@jira_measure("locust_add_comment_trigger_outbound_notification")
def add_comment_trigger_outbound_notification(locust):
    params = AddComment()
    issue_id = 2013912
    issue_key = "DEV-6"
    project_key = "DEV"

    @jira_measure('locust_add_comment_trigger_outbound_notification:open_comment')
    def add_comment_open_comment():
        raise_if_login_failed(locust)
        r = locust.get(f'/secure/AddComment!default.jspa?id={issue_id}', catch_response=True)
        content = r.content.decode('utf-8')
        token = fetch_by_re(params.atl_token_pattern, content)
        form_token = fetch_by_re(params.form_token_pattern, content)
        if not (f'Add Comment: {issue_key}' in content):
            logger.error(f'Could not open comment in the {issue_key} issue: {content}')
        assert f'Add Comment: {issue_key}' in content, 'Could not open comment in the issue'

        locust.post('/rest/webResources/1.0/resources', json=params.resources_body.get("805"),
                    headers=RESOURCE_HEADERS, catch_response=True)
        locust.post('/rest/webResources/1.0/resources', json=params.resources_body.get("810"),
                    headers=RESOURCE_HEADERS, catch_response=True)
        locust.post('/rest/webResources/1.0/resources', json=params.resources_body.get("820"),
                    headers=RESOURCE_HEADERS, catch_response=True)
        locust.get(f'/rest/internal/2/user/mention/search?issueKey={issue_key}&projectKey={project_key}'
                   f'&maxResults=10&_={timestamp_int()}', catch_response=True)
        locust.session_data_storage['token'] = token
        locust.session_data_storage['form_token'] = form_token
    add_comment_open_comment()

    @jira_measure('locust_add_comment_trigger_outbound_notification:save_comment')
    def add_comment_save_comment():
        raise_if_login_failed(locust)
        r = locust.post(f'/secure/AddComment.jspa?atl_token={locust.session_data_storage["token"]}',
                        params={"id": {issue_id}, "formToken": locust.session_data_storage["form_token"],
                                "dnd-dropzone": None, "comment": generate_random_string(20),
                                "commentLevel": None, "atl_token": locust.session_data_storage["token"],
                                "Add": "Add"}, headers=TEXT_HEADERS, catch_response=True)
        content = r.content.decode('utf-8')
        if not (f'<meta name="ajs-issue-key" content="{issue_key}">' in content):
            logger.error(f'Could not save comment: {content}')
        assert f'<meta name="ajs-issue-key" content="{issue_key}">' in content, 'Could not save comment'
    add_comment_save_comment()
