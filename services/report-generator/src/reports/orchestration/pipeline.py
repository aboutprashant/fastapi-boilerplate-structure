class ReportPipeline:
    """Pipeline stub. Code migrates here from the legacy repo."""

    async def interpret(self, prompt: str) -> dict:
        return {"prompt": prompt}

    async def resolve(self, interpreted: dict) -> dict:
        return interpreted

    async def plan(self, resolved: dict) -> dict:
        return resolved

    async def fetch(self, plan: dict) -> dict:
        return plan

    async def generate(self, inputs: dict) -> dict:
        return inputs

    async def render(self, generated: dict) -> dict:
        return {"download_url": "/mock/report.pdf", "manifest": generated}

    async def run(self, prompt: str) -> dict:
        interpreted = await self.interpret(prompt)
        resolved = await self.resolve(interpreted)
        plan = await self.plan(resolved)
        fetched = await self.fetch(plan)
        generated = await self.generate(fetched)
        return await self.render(generated)
