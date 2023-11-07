import traceback
import typing as t

from ansible.plugins.action import ActionBase

__all__ = [
    "ActionModule",
]


class ActionModule(ActionBase):
    """Check play variables by schema dictionary"""

    def _check_level_recursively(
        self,
        name: str,
        level_vars: t.Any,  # typically it's a dict
        level_schema: t.Any,  # typically it's a dict too
        is_templated: bool,
        warnings_list: t.List[str],
    ) -> None:
        # User input, so it's better to check
        if not isinstance(level_schema, dict):
            raise ValueError(f"Not a dict schema: {level_schema!r}")
        if not isinstance(level_vars, dict):
            # TODO: should we raise an error here?
            return
        for schema_key, sub_level_schema in level_schema.items():
            sub_level_name: str = schema_key if not name else f"{name}.{schema_key}"
            if isinstance(sub_level_schema, dict):
                # Whenever the schema node is a dict, we go deeper
                sub_level_vars: t.Any = level_vars.get(schema_key)
                if sub_level_vars and not is_templated:
                    sub_level_vars = self._templar.template(sub_level_vars)
                    is_templated = True
                self._check_level_recursively(
                    name=sub_level_name,
                    level_vars=sub_level_vars or {},
                    level_schema=sub_level_schema,
                    is_templated=is_templated,
                    warnings_list=warnings_list,
                )
            elif isinstance(sub_level_schema, str):
                if not (isinstance(level_vars, dict) and schema_key in level_vars):
                    warnings_list.append(f"Missing variable {sub_level_name}: {sub_level_schema}")
            else:
                raise ValueError(f"Schema node value is neither a dict nor a string: {sub_level_schema}")

    def _check_schema(self, task_vars: t.Optional[dict]) -> dict:
        try:
            schema: dict = self._task.args.pop("schema", {})
            if not schema:
                return {
                    "failed": True,
                    "msg": "No schema was provided",
                    "changed": False,
                }
            warnings_list: list[str] = []
            upper_level_vars: dict = (task_vars or {}).get("vars", {})
            self._check_level_recursively(
                name="",
                level_vars=upper_level_vars,
                level_schema=schema,
                is_templated=False,
                warnings_list=warnings_list,
            )
            return {
                "failed": bool(warnings_list),
                "msg": f"Failed assertions count: {len(warnings_list)}",
                "changed": False,
                "warnings": warnings_list,
            }
        except Exception as e:
            self._display.vvv(traceback.format_exc())
            return {
                "failed": True,
                "msg": traceback.format_exception_only(type(e), e)[-1].strip(),
                "changed": False,
            }

    def run(self, tmp: t.Optional[str] = None, task_vars: t.Optional[dict] = None) -> dict:
        return {
            **super().run(tmp=tmp, task_vars=task_vars),
            **self._check_schema(task_vars=task_vars),
        }
