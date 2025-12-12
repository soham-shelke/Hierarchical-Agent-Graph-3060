import requests
import json
import time

# --- CONFIGURATION ---
OLLAMA_URL = "http://localhost:11434/api/chat"
MANAGER_MODEL = "llama3.2"       # 3B Model
WORKER_MODEL = "llama3.2:1b"     # 1B Model
TASK = "Write a Python script for a simple Snake game using the pygame library."

# --- HELPER FUNCTION TO CALL OLLAMA ---
def chat_with_ollama(model, messages):
    payload = {
        "model": model,
        "messages": messages,
        "stream": False,
        "options": {
            "num_ctx": 4096,  # Force context window size
            "temperature": 0.2
        }
    }
    start_time = time.time()
    try:
        response = requests.post(OLLAMA_URL, json=payload).json()
        duration = time.time() - start_time
        
        # Extract content and token counts (Ollama returns these stats)
        content = response['message']['content']
        prompt_eval_count = response.get('prompt_eval_count', 0)
        eval_count = response.get('eval_count', 0)
        
        return content, duration, prompt_eval_count, eval_count
    except Exception as e:
        print(f"Error calling Ollama: {e}")
        return "", 0, 0, 0

# --- EXPERIMENT 1: STANDARD LINEAR WORKFLOW (BASELINE) ---
def run_linear_workflow():
    print(f"\n[BASELINE] Running Standard Linear History Workflow...")
    messages = [
        {"role": "system", "content": "You are a Manager Agent. Break the task down and ask the Worker to do it step by step."}
    ]
    
    total_duration = 0
    total_tokens_processed = 0
    
    # Step 1: Manager plans
    messages.append({"role": "user", "content": f"Task: {TASK}"})
    response, dur, p_tok, g_tok = chat_with_ollama(MANAGER_MODEL, messages)
    total_duration += dur
    total_tokens_processed += (p_tok + g_tok)
    messages.append({"role": "assistant", "content": response})
    print(f" > Manager planned ({dur:.2f}s). Context size: {p_tok} tokens.")

    # Step 2: Worker executes (Uses FULL history)
    # We simulate the worker seeing the whole conversation to understand context
    worker_messages = messages.copy() 
    worker_messages.append({"role": "user", "content": "Worker, please execute the first phase of this plan."})
    
    response, dur, p_tok, g_tok = chat_with_ollama(WORKER_MODEL, worker_messages)
    total_duration += dur
    total_tokens_processed += (p_tok + g_tok)
    print(f" > Worker executed ({dur:.2f}s). Context size: {p_tok} tokens.")
    
    return total_duration, total_tokens_processed

# --- EXPERIMENT 2: GRAPH-BASED WORKFLOW (YOUR METHOD) ---
def run_graph_workflow():
    print(f"\n[PROPOSED] Running Graph-Based (Context Pruned) Workflow...")
    
    total_duration = 0
    total_tokens_processed = 0
    
    # Step 1: Manager Plans (Same as baseline, but we parse it into a 'Graph Node')
    # We tell the manager to output ONLY the specific instruction for the next node
    manager_messages = [
        {"role": "system", "content": "You are a Manager. Output ONLY the technical instruction for the first step of this task. Do not explain."}
    ]
    manager_messages.append({"role": "user", "content": f"Task: {TASK}"})
    
    node_instruction, dur, p_tok, g_tok = chat_with_ollama(MANAGER_MODEL, manager_messages)
    total_duration += dur
    total_tokens_processed += (p_tok + g_tok)
    print(f" > Manager generated Graph Node 1 ({dur:.2f}s). Context size: {p_tok} tokens.")
    
    # Step 2: Worker Executes (Graph Mode)
    # CRITICAL: Worker DOES NOT see the Manager's system prompt or previous history.
    # Worker sees ONLY the current Node Instruction.
    worker_messages = [
        {"role": "system", "content": "You are a Python coding worker. Write code based on the instruction."},
        {"role": "user", "content": node_instruction} # Only the specific node!
    ]
    
    response, dur, p_tok, g_tok = chat_with_ollama(WORKER_MODEL, worker_messages)
    total_duration += dur
    total_tokens_processed += (p_tok + g_tok)
    print(f" > Worker executed Node 1 ({dur:.2f}s). Context size: {p_tok} tokens.")
    
    return total_duration, total_tokens_processed

# --- MAIN COMPARISON ---
if __name__ == "__main__":
    print(f"--- STARTING EXPERIMENT ON {torch.cuda.get_device_name(0) if 'torch' in locals() else 'LOCAL GPU'} ---")
    
    # Run Baseline
    base_time, base_tokens = run_linear_workflow()
    
    # Run Proposed
    graph_time, graph_tokens = run_graph_workflow()
    
    # Calculate Improvements
    time_diff = base_time - graph_time
    token_diff = base_tokens - graph_tokens
    token_reduction_pct = (token_diff / base_tokens) * 100
    
    print("\n" + "="*40)
    print("       EXPERIMENTAL RESULTS")
    print("="*40)
    print(f"{'Metric':<20} | {'Baseline':<10} | {'Graph (Yours)':<10}")
    print("-" * 45)
    print(f"{'Duration (sec)':<20} | {base_time:<10.2f} | {graph_time:<10.2f}")
    print(f"{'Total Tokens':<20} | {base_tokens:<10} | {graph_tokens:<10}")
    print("-" * 45)
    print(f"EFFICIENCY GAIN: {token_reduction_pct:.2f}% reduction in processing load.")
    print("="*40)