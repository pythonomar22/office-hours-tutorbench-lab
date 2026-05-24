# Public HF Agentic v11c Full Run Status

Run ID: `publichf-agentic-v11c-full`

Status: interrupted by Anthropic account usage cap before full generation finished.

## Configuration

- Dataset revision: `c70d2311cdca7129cab9376ba22eaa97c3cff3d7`
- Dataset scope: public Hugging Face set, 1,473 examples
- Strategy: `agentic`
- Prompt version: `agentic-v11`
- Candidate model: `anthropic:claude-sonnet-4-6`
- Solver/planner/verifier/critic model: `anthropic:claude-sonnet-4-6`
- Max tokens: `2200`
- Max revision attempts: `2`
- Final stable worker count before cap: `8`

## Completed Responses

Generated responses written to private raw trace file: `650 / 1,473`.

Completed slice:

| Use case | Modality | Count |
| --- | --- | ---: |
| adaptive | text | 327 |
| adaptive | multimodal | 146 |
| assessment | multimodal | 177 |

No judgments or full-set scores were produced for this run, because the same Claude-family access is required for the calibrated judge.

## Attempts

The initial 24-worker attempt reached `174` completed responses, then produced transient `APIConnectionError` failures. That error log is retained privately as `errors.attempt24workers.jsonl`.

The resumed 8-worker attempt was stable through the text-heavy portion and much of the multimodal portion, then stopped when Anthropic returned a hard account usage-cap error:

`You have reached your specified API usage limits. You will regain access on 2026-06-01 at 00:00 UTC.`

The second attempt wrote `60` private error records, all wrapped as retry failures after the account cap was reached.

## Fairness Note

This is not yet a comparable full public-HF score and not a leaderboard-exact submission. It is a partial generation run only. The public-HF set also differs from the Scale leaderboard set reported publicly: public HF has 1,473 examples, while the leaderboard describes 1,490 examples.

## Next Resume Command

Once Anthropic access is restored or a higher-cap Sonnet key is available, resume generation from the existing raw responses:

```bash
uv run tutorbench-lab run \
  --strategy agentic \
  --run-id publichf-agentic-v11c-full \
  --model anthropic:claude-sonnet-4-6 \
  --solver-model anthropic:claude-sonnet-4-6 \
  --planner-model anthropic:claude-sonnet-4-6 \
  --verifier-model anthropic:claude-sonnet-4-6 \
  --critic-model anthropic:claude-sonnet-4-6 \
  --max-tokens 2200 \
  --max-revision-attempts 2 \
  --request-timeout-s 240 \
  --workers 4 \
  --resume
```

Use `--workers 4` for the next multimodal-heavy resume unless the Anthropic account limit is raised substantially.
