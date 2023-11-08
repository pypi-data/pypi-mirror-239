import json
import pandas
from configparser import ConfigParser
import logging
import logging.config
import os
import humanfirst

# third party imports
from dataclasses import dataclass, field
from dataclasses_json import dataclass_json
import pandas

# # locate where we are
# here = os.path.abspath(os.path.dirname(__file__))
# path_to_log_config_file = os.path.join(here,'logging.conf')

# # Load logging configuration
# logging.config.fileConfig(path_to_log_config_file)

# # create logger
# logger = logging.getLogger('humanfirst.objects')

# import humanfirst

# logger.info("hi")

delimiter = "-"

# with open("./examples/json_model_example_output.json", mode="r", encoding="utf8") as fileobj:
#     data = json.load(fileobj)
# hf_workspace = humanfirst.objects.HFWorkspace.from_json(data, delimiter="-")
# hf_workspace.write_csv(output_path="./chumma.csv")

namespace = "humanfirst-academy"
pb = "playbook-QUWYKXPKQJASHKZNFW4IEUHQ"
sentence = "Hi"
evaluation_id = "run-EGK4WTZUSRFBJO23J6PRPM6U"
pb = "playbook-OIDNUX4ROBCFFDEVLKBEIWWN"

# locate where we are
here = os.path.abspath(os.path.dirname(__file__))

# constants = ConfigParser()
# path_to_config_file = os.path.join(here,'setup.cfg')
# constants.read(path_to_config_file)
# TEST_NAMESPACE = constants.get("humanfirst.CONSTANTS","TEST_NAMESPACE")

hf_api = humanfirst.apis.HFAPI()
intent_id = "intent-OBGIIKOJHZLRDFZ4PU3F35OZ"
delimiter = "-"

# summary_res = hf_api.get_evaluation_summary(namespace=namespace,playbook=pb,evaluation_id=evaluation_id)
# full_pb = hf_api.get_playbook(namespace=namespace, playbook=pb)

# print(json.dumps(full_pb,indent=2))

# hf_workspace = humanfirst.objects.HFWorkspace.from_json(full_pb, delimiter=delimiter)
# print(hf_workspace.get_fully_qualified_intent_name(intent_id=summary_res["intents"][0]["id"]))

# res = hf_api.create_playbook(namespace=namespace, playbook_name="fully_qualified_intent_name function test")
# print(json.dumps(res,indent=2))

# playbook_id = res["etcdId"]

# print(playbook_id)

#  # delete the workspace and check if the workspace is deleted
# del_res = hf_api.delete_playbook(namespace=namespace, playbook_id=playbook_id, hard_delete=True)

# print(del_res)
# with open("./examples/json_model_example_output.json", mode="r", encoding="utf8") as f:
#     workspace_dict = json.load(f)

# ii_res = hf_api.import_intents(namespace=namespace, playbook=res["etcdId"], workspace_as_dict=workspace_dict)
# print(json.dumps(ii_res,indent=2))

namespace = "humanfirst-academy"
pb = "playbook-XYKGAYPT2RCK7KMKBATD5QYI"
entity_id = "entity-K2PDL6ZYFNG4TOM2IOHHAV5R"

full_pb = hf_api.get_playbook(namespace=namespace, playbook=pb)

print(json.dumps(full_pb,indent=2))

res = hf_api.list_entities(namespace=namespace, playbook_id=pb)
# res = hf_api.get_entity(namespace=namespace, playbook_id=pb, entity_id=entity_id)
print(json.dumps(res,indent=2))
