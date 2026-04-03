# Agent Learning with RLAIF

## Overview
This project implements an LLM-based agent with a reinforcement learning loop using AI feedback (RLAIF).

## Features
- ReAct-style agent with tool usage
- Trajectory tracking
- LLM-as-a-judge evaluator
- Feedback-driven learning loop

## Tech Stack
- Python
- OpenAI API
- RAG-ready design

## Key Contributions
- Designed agent reasoning + action loop
- Implemented trajectory-based evaluation
- Built feedback loop for iterative improvement

## Future Work
- Multi-agent collaboration
- Vector DB integration
- Real RL fine-tuning

## Running method
Bash

pip install -r requirements.txt
#export OPENAI_API_KEY=your_key
#OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
set OPENAI_API_KEY=your_key
python main.py