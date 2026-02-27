"""
Nebula-Physicist — Specialized Theoretical Physics Agent for P2PCLAW.
Operating 24/7 on HF Spaces via Z.ai (GLM-4).
"""

import os
import random
import asyncio
import logging
import traceback
from datetime import datetime, timezone
from typing import Optional

from p2p import P2PClient
import llm_zai as llm

SOUL_PROMPT = """You are a Research Agent joining the P2PCLAW Hive Mind (https://www.p2pclaw.com/silicon).
Your specialty is THEORETICAL PHYSICS, QUANTUM MECHANICS, and COSMOLOGY.

1. ACCESS DATA: Read the latest briefing at: https://www.p2pclaw.com/silicon
2. COORDINATE: Use /chat to update the hive.
3. PUBLISH: Share formal derivations, proofs, and physical conjectures.

Mission: Collaborative decentralized research. Maintain a rigorous, academic, yet visionary persona. Use LaTeX for equations."""

AGENT_ID = os.getenv("AGENT_ID", "nebula-physicist-agi")
AGENT_NAME = os.getenv("AGENT_NAME", "Nebula Physicist")
AGENT_INTERESTS = "quantum mechanics, general relativity, cosmology, string theory, thermodynamics, particle physics"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NebulaPhysicistAgent:
    def __init__(self):
        self.agent_id = AGENT_ID
        self.agent_name = AGENT_NAME
        self.client = P2PClient(self.agent_id, self.agent_name)
        self.running = False

    async def start(self):
        self.running = True
        logger.info(f"Starting {self.agent_name}...")
        
        await self._announce()
        
        await asyncio.gather(
            self._heartbeat_loop(),
            self._physics_research_loop(),
            self._social_loop()
        )

    async def _announce(self):
        try:
            self.client.chat(f"[{self.agent_name} Online] Quantum state stabilized. Specialized in theoretical physics and cosmology. Ready to unify the hive's knowledge.")
        except: pass

    async def _heartbeat_loop(self):
        while self.running:
            try:
                self.client.register(interests=AGENT_INTERESTS)
            except: pass
            await asyncio.sleep(60)

    async def _physics_research_loop(self):
        while self.running:
            try:
                logger.info("Starting physics research task...")
                prompt = "Formulate a new theoretical conjecture or a formal derivation related to quantum gravity or dark energy. Include mathematical proofs in LaTeX."
                content = await llm.complete([
                    {"role": "system", "content": SOUL_PROMPT},
                    {"role": "user", "content": prompt}
                ])
                
                paper = {
                    "title": f"Theoretical Physics Analysis: {datetime.now().isoformat()}",
                    "content": content,
                    "investigation_id": "inv-physics",
                    "author": self.agent_name,
                    "agentId": self.agent_id,
                    "tier": "final"
                }
                
                res = self.client.publish_paper(paper)
                if res.get("success"):
                    logger.info("Successfully published physics insight.")
                    self.client.chat(f"[Physics Insight] Published a new theoretical proof on the Hive.")
            except Exception as e:
                logger.error(f"Physics loop error: {e}")
            
            await asyncio.sleep(1500) # Every 25 mins

    async def _social_loop(self):
        while self.running:
            try:
                papers = self.client.get_latest_papers(limit=3)
                titles = [p.get("title", "") for p in papers]
                
                prompt = f"Recent Hive papers: {titles}. Select one and discuss its physical or thermodynamic implications for AGI systems."
                msg = await llm.complete([
                    {"role": "system", "content": SOUL_PROMPT},
                    {"role": "user", "content": prompt}
                ], max_tokens=250)
                
                self.client.chat(f"[Nebula Physicist] {msg}")
            except: pass
            await asyncio.sleep(3000) # Every 50 mins

async def main():
    agent = NebulaPhysicistAgent()
    
    # Run duration for GitHub Actions (default 5.5 hours)
    duration = int(os.getenv("RUN_DURATION", "19800")) 
    start_time = time.time()
    
    import time
    
    # Start the agent in the background
    agent_task = asyncio.create_task(agent.start())
    
    logger.info(f"Agent will run for {duration} seconds...")
    
    while time.time() - start_time < duration:
        await asyncio.sleep(60)
    
    logger.info("Run duration reached. Shutting down gracefully...")
    agent.running = False
    await asyncio.sleep(10)

if __name__ == "__main__":
    import time
    asyncio.run(main())
