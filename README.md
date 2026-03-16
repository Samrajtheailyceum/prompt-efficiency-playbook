# The Prompt Efficiency Playbook

**How to Make Claude Faster, Cheaper, and Better: Primary Research with 55 Controlled Experiments**

*By Samraj Matharu | [The AI Lyceum](mailto:hello@theailyceum.com) | 16 March 2026*

---

## Key Finding

A single formatting instruction cut Claude's output tokens by **73.9%**, saving **$71 for every $100 spent** on Claude Opus output. No clever persona prompts. No complex chains. Just one line:

```
"Respond in exactly 3 bullet points. Each bullet must be under 25 words. No preamble, no conclusion."
```

## What This Research Is

I ran **55 controlled API experiments** against Claude Haiku 4.5, testing 11 prompt configurations across 5 knowledge domains (Business, Science, Technology, Finance, History). Every token was measured. Every result is reproducible.

This repo contains:
- The full research paper (HTML + PDF)
- The Python experiment script (run it yourself)
- Raw JSON results from all 55 API calls
- 7 data visualisation charts

## Five Key Findings

| # | Finding | Data |
|---|---------|------|
| 1 | **Format beats persona.** Output format constraints cut tokens by 73.9%. Persona prompts *increased* output. | T5 vs T1: 89.8 vs 418.8 tokens |
| 2 | **One technique is enough.** Stacking 6 techniques performed *worse* than the single best technique alone. | Full Stack: 107.4 tokens vs T5 alone: 89.8 |
| 3 | **Saves $172,000/year at scale.** An enterprise running 100K daily Opus queries saves ~$172K annually. | See Section VII |
| 4 | **57% faster responses.** Shorter outputs = faster replies: 4.16s down to 1.79s. | See Section VI |
| 5 | **74% less energy per query.** Fewer tokens = less electricity, less water, less carbon. | See Section X |

## Results at a Glance

| Technique | Avg Output Tokens | Change | Cost per Query (Opus) |
|-----------|------------------|--------|----------------------|
| Baseline (no prompting) | 344.0 | - | $0.0086 |
| T1: Role Specialist | 418.8 | +21.7% | $0.0105 |
| T2: XML Tags | 366.4 | +6.5% | $0.0092 |
| T3: Few-Shot Examples | 340.6 | -1.0% | $0.0085 |
| T4: Concise CoT | 310.2 | -9.8% | $0.0078 |
| **T5: Output Format** | **89.8** | **-73.9%** | **$0.0022** |
| T6: Positive Framing | 388.2 | +12.8% | $0.0097 |

## Read the Full Paper

**[Download the PDF](The-Prompt-Efficiency-Playbook.pdf)** | **[View the HTML](The-Prompt-Efficiency-Playbook.html)**

## Reproduce the Experiments

```bash
# Set your Anthropic API key
export ANTHROPIC_API_KEY="your-key-here"

# Install the Anthropic SDK
pip install anthropic

# Run all 55 experiments (~$0.15 total cost on Haiku)
python prompt_experiments.py
```

Results are saved to `prompt_experiment_results.json`.

## Repository Contents

```
prompt-efficiency-playbook/
  The-Prompt-Efficiency-Playbook.pdf   # Full research paper
  The-Prompt-Efficiency-Playbook.html  # Source HTML (branded)
  prompt_experiments.py                # Python experiment script
  prompt_experiment_results.json       # Raw results (all 55 calls)
  fig1_primary_output_tokens.png       # Output tokens by technique
  fig2_primary_word_counts.png         # Word counts by technique
  fig3_primary_response_time.png       # Response times
  fig4_primary_heatmap.png             # Heatmap: tokens x domains
  fig5_primary_cumulative.png          # Stacking effects
  fig6_primary_environmental.png       # Environmental impact
  fig7_primary_dashboard.png           # Summary dashboard
  ai-lyceum-logo.png                   # The AI Lyceum logo
```

## Who This Is For

- **Engineering teams** building with Claude, GPT-4, or similar APIs
- **Product managers** looking to reduce AI infrastructure costs
- **AI agent developers** where every API call compounds cost and latency
- **Anyone** who pays for AI tokens and wants to pay less

## Citation

```
Matharu, S. (2026). "The Prompt Efficiency Playbook: How to Make Claude
Faster, Cheaper, and Better." The AI Lyceum, 16 March 2026.
```

## Contact

**Samraj Matharu** | Founder, The AI Lyceum
hello@theailyceum.com

---

## License & Copyright

Copyright 2026 Samraj Matharu / The AI Lyceum. All rights reserved.

No part of this publication may be reproduced, distributed, or transmitted in any form without the prior written permission of the author, except for brief quotations in reviews and academic citations.

The AI Lyceum is a registered trademark of Samraj Matharu.

Published 16 March 2026.
