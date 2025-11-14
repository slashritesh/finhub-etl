"""
Task Processor

Processes different types of tasks received from RabbitMQ.
"""

import importlib
import httpx
from typing import Any, Dict
from .schemas import Task, FetchTask, UrlFetchTask, BulkFetchTask, GenericTask
from worker.utils.save import fetch_and_store_data


class TaskProcessor:
    """Processes tasks based on their type."""

    def __init__(self):
        self.handlers_cache = {}
        self.models_cache = {}

    async def process(self, task: Task) -> Dict[str, Any]:
        """
        Process a task based on its type.

        Args:
            task: Validated task object

        Returns:
            Dictionary with processing result
        """
        print(f"📋 Processing task: {task.task_id} (type: {task.task_type})")

        try:
            if isinstance(task, FetchTask):
                result = await self._process_fetch_task(task)
            elif isinstance(task, UrlFetchTask):
                result = await self._process_url_task(task)
            elif isinstance(task, BulkFetchTask):
                result = await self._process_bulk_task(task)
            elif isinstance(task, GenericTask):
                result = await self._process_generic_task(task)
            else:
                raise ValueError(f"Unknown task type: {type(task)}")

            print(f"✅ Task {task.task_id} completed successfully")
            return {"status": "success", "task_id": task.task_id, "result": result}

        except Exception as e:
            print(f"❌ Task {task.task_id} failed: {str(e)}")
            return {"status": "error", "task_id": task.task_id, "error": str(e)}

    async def _process_fetch_task(self, task: FetchTask) -> Any:
        """Process a Finnhub API fetch task."""
        # Map task types to handlers and models
        task_mapping = {
            "fetch_company_profile": {
                "handler": "worker.config.handlers.company.get_company_profile2",
                "model": "worker.models.company_profile.CompanyProfile2",
            },
            "fetch_quote": {
                "handler": "worker.config.handlers.trading.get_quote",
                "model": "worker.models.quote.Quote",
            },
            # Add more mappings as needed
        }

        if task.task_type not in task_mapping:
            raise ValueError(f"Unknown fetch task type: {task.task_type}")

        mapping = task_mapping[task.task_type]
        handler = self._get_handler(mapping["handler"])
        model = self._get_model(mapping["model"])

        # Merge symbol and additional params
        params = {"symbol": task.symbol, **task.params}

        # Use the existing fetch_and_store_data utility
        result = await fetch_and_store_data(
            handler=handler,
            model=model,
            **params
        )

        return result

    async def _process_url_task(self, task: UrlFetchTask) -> Any:
        """Process a direct URL fetch task."""
        async with httpx.AsyncClient() as client:
            if task.method == "GET":
                response = await client.get(
                    task.url,
                    headers=task.headers,
                    params=task.params,
                    timeout=30.0
                )
            else:  # POST
                response = await client.post(
                    task.url,
                    headers=task.headers,
                    json=task.params,
                    timeout=30.0
                )

            response.raise_for_status()
            return response.json()

    async def _process_bulk_task(self, task: BulkFetchTask) -> list[Any]:
        """Process a bulk fetch task for multiple symbols."""
        results = []

        for symbol in task.symbols:
            try:
                # Create individual fetch task for each symbol
                individual_task = FetchTask(
                    task_id=f"{task.task_id}_{symbol}",
                    task_type=f"fetch_{task.data_type}",
                    symbol=symbol,
                    params={
                        **({"from_date": task.from_date} if task.from_date else {}),
                        **({"to_date": task.to_date} if task.to_date else {}),
                        **task.extra_params,
                    },
                )
                result = await self._process_fetch_task(individual_task)
                results.append({"symbol": symbol, "status": "success", "data": result})
            except Exception as e:
                print(f"⚠️ Failed to fetch {symbol}: {str(e)}")
                results.append({"symbol": symbol, "status": "error", "error": str(e)})

        return results

    async def _process_generic_task(self, task: GenericTask) -> Any:
        """Process a generic task with custom handler and model."""
        handler = self._get_handler(f"worker.config.handlers.{task.handler}")
        model = self._get_model(f"worker.models.{task.model}")

        result = await fetch_and_store_data(
            handler=handler,
            model=model,
            **task.params
        )

        return result

    def _get_handler(self, handler_path: str):
        """
        Dynamically import and cache a handler function.

        Args:
            handler_path: Dotted path to handler (e.g., 'worker.config.handlers.company.get_company_profile2')
        """
        if handler_path in self.handlers_cache:
            return self.handlers_cache[handler_path]

        module_path, function_name = handler_path.rsplit(".", 1)
        module = importlib.import_module(module_path)
        handler = getattr(module, function_name)

        self.handlers_cache[handler_path] = handler
        return handler

    def _get_model(self, model_path: str):
        """
        Dynamically import and cache a model class.

        Args:
            model_path: Dotted path to model (e.g., 'worker.models.company_profile.CompanyProfile2')
        """
        if model_path in self.models_cache:
            return self.models_cache[model_path]

        module_path, class_name = model_path.rsplit(".", 1)
        module = importlib.import_module(module_path)
        model = getattr(module, class_name)

        self.models_cache[model_path] = model
        return model


# Global processor instance
processor = TaskProcessor()
