"""

"""


import phantom.rules as phantom
import json
from datetime import datetime, timedelta


@phantom.playbook_block()
def on_start(container):
    phantom.debug('on_start() called')

    # call 'decision_1' block
    decision_1(container=container)
    # call 'debug_1' block
    debug_1(container=container)
    # call 'set_custom_fields_1' block
    set_custom_fields_1(container=container)

    return

@phantom.playbook_block()
def update_finding_or_investigation_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("update_finding_or_investigation_1() called")

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    finding_data = phantom.collect2(container=container, datapath=["finding:finding_id"])
    prompt_for_finding_owner_result_data = phantom.collect2(container=container, datapath=["prompt_for_finding_owner:action_result.summary.responses.0","prompt_for_finding_owner:action_result.parameter.context.artifact_id"], action_results=results)

    parameters = []

    # build parameters list for 'update_finding_or_investigation_1' call
    for finding_data_item in finding_data:
        for prompt_for_finding_owner_result_item in prompt_for_finding_owner_result_data:
            if finding_data_item[0] is not None:
                parameters.append({
                    "id": finding_data_item[0],
                    "owner": prompt_for_finding_owner_result_item[0],
                })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.act("update finding or investigation", parameters=parameters, name="update_finding_or_investigation_1", assets=["builtin_mc_connector"], callback=join_prompt_for_final_note)

    return


@phantom.playbook_block()
def prompt_for_finding_owner(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("prompt_for_finding_owner() called")

    # set approver and message variables for phantom.prompt call

    user = phantom.collect2(container=container, datapath=["playbook:launching_user.name"])[0][0]
    role = None
    message = """About to close finding."""

    # parameter list for template variable replacement
    parameters = []

    # responses
    response_types = [
        {
            "prompt": "Please enter the Finding owner",
            "options": {
                "type": "message",
                "required": True,
            },
        }
    ]

    phantom.prompt2(container=container, user=user, role=role, message=message, respond_in_mins=30, name="prompt_for_finding_owner", parameters=parameters, response_types=response_types, callback=update_finding_or_investigation_1)

    return


@phantom.playbook_block()
def decision_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("decision_1() called")

    # check for 'if' condition 1
    found_match_1 = phantom.decision(
        container=container,
        conditions=[
            ["finding:owner", "is None"]
        ],
        conditions_dps=[
            ["finding:owner", "is None"]
        ],
        name="decision_1:condition_1",
        delimiter=None)

    # call connected blocks if condition 1 matched
    if found_match_1:
        prompt_for_finding_owner(action=action, success=success, container=container, results=results, handle=handle)
        return

    # check for 'else' condition 2
    join_prompt_for_final_note(action=action, success=success, container=container, results=results, handle=handle)

    return


@phantom.playbook_block()
def debug_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("debug_1() called")

    finding_data = phantom.collect2(container=container, datapath=["finding:owner"])

    finding_owner = [item[0] for item in finding_data]

    parameters = []

    parameters.append({
        "input_1": finding_owner,
        "input_2": ["owner"],
        "input_3": None,
        "input_4": None,
        "input_5": None,
        "input_6": None,
        "input_7": None,
        "input_8": None,
        "input_9": None,
        "input_10": None,
    })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.custom_function(custom_function="community/debug", parameters=parameters, name="debug_1")

    return


@phantom.playbook_block()
def join_prompt_for_final_note(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("join_prompt_for_final_note() called")

    if phantom.completed(action_names=["update_finding_or_investigation_1"]):
        # call connected block "prompt_for_final_note"
        prompt_for_final_note(container=container, handle=handle)

    return


@phantom.playbook_block()
def prompt_for_final_note(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("prompt_for_final_note() called")

    # set approver and message variables for phantom.prompt call

    user = phantom.collect2(container=container, datapath=["playbook:launching_user.name"])[0][0]
    role = None
    message = """Closing a Finding requires a final note"""

    # parameter list for template variable replacement
    parameters = []

    # responses
    response_types = [
        {
            "prompt": "Please enter a Title for the final note",
            "options": {
                "type": "message",
                "required": True,
            },
        },
        {
            "prompt": "Please enter the notes here",
            "options": {
                "type": "message",
                "required": True,
            },
        }
    ]

    phantom.prompt2(container=container, user=user, role=role, message=message, respond_in_mins=30, name="prompt_for_final_note", parameters=parameters, response_types=response_types, callback=add_finding_or_investigation_note_3)

    return


@phantom.playbook_block()
def add_finding_or_investigation_note_3(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("add_finding_or_investigation_note_3() called")

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    finding_data = phantom.collect2(container=container, datapath=["finding:finding_id"])
    prompt_for_final_note_result_data = phantom.collect2(container=container, datapath=["prompt_for_final_note:action_result.summary.responses.0","prompt_for_final_note:action_result.summary.responses.1","prompt_for_final_note:action_result.parameter.context.artifact_id"], action_results=results)

    parameters = []

    # build parameters list for 'add_finding_or_investigation_note_3' call
    for finding_data_item in finding_data:
        for prompt_for_final_note_result_item in prompt_for_final_note_result_data:
            if finding_data_item[0] is not None and prompt_for_final_note_result_item[1] is not None:
                parameters.append({
                    "id": finding_data_item[0],
                    "title": prompt_for_final_note_result_item[0],
                    "content": prompt_for_final_note_result_item[1],
                })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.act("add finding or investigation note", parameters=parameters, name="add_finding_or_investigation_note_3", assets=["builtin_mc_connector"], callback=close_finding)

    return


@phantom.playbook_block()
def close_finding(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("close_finding() called")

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    finding_data = phantom.collect2(container=container, datapath=["finding:finding_id"])

    parameters = []

    # build parameters list for 'close_finding' call
    for finding_data_item in finding_data:
        if finding_data_item[0] is not None:
            parameters.append({
                "id": finding_data_item[0],
                "status": "Closed",
            })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.act("update finding or investigation", parameters=parameters, name="close_finding", assets=["builtin_mc_connector"])

    return


@phantom.playbook_block()
def set_custom_fields_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("set_custom_fields_1() called")

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    finding_data = phantom.collect2(container=container, datapath=["finding:finding_id"])

    parameters = []

    # build parameters list for 'set_custom_fields_1' call
    for finding_data_item in finding_data:
        if finding_data_item[0] is not None:
            parameters.append({
                "incident_id": finding_data_item[0],
                "pairs": [
                    { "name": "Department", "value": "HR" },
                ],
            })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.act("set custom fields", parameters=parameters, name="set_custom_fields_1", assets=["builtin_mc_connector"])

    return


@phantom.playbook_block()
def on_finish(container, summary):
    phantom.debug("on_finish() called")

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    return