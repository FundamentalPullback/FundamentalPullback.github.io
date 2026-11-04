# Stage 3.5 publication consistency

Eligibility for technical assessment is separate from entry authorization and existing holdings. A researcher must first make the assessment; these tools do not ingest market news or authorize trades.

1. Update the structured assessment ticket and its matching record in `data/stage35-assessments.json`. The ticker, report ID, analysis date and publication contract must agree.
2. Read the actual canonical Sheet using the authorized connector. Save a private snapshot outside the public site. Use either an unfiltered contiguous range with `contiguous: true` and `startRowIndex`, or exact `rowIndices` for every returned row, including the header. Never infer row numbers after filtering. Google Sheets date serials are supported.
3. Run `python tools/stage35-publication.py plan --site-root SITE --sheet-snapshot PRIVATE_SNAPSHOT --output PRIVATE_OUTPUT`. Review the generated minimal Sheet payload and projected decisions. Apply the Sheet changes through the authorized connector, then use `apply-local` with the same inputs. Holdings and unrelated decision fields are never changed.
4. Read the actual Sheet again after writing. Save private evidence with `source: google-sheets-readback`, an actual ISO `capturedAt`, and `values` containing the returned header and decision rows. Do not substitute the planned payload for read-back.
5. Run the existing `tools/prepare-publication.py` with `STAGE35_SHEET_READBACK` pointing to that private evidence. Publication preparation fails when ticket, registry, local decision or Sheet status disagree. It also runs generic future-symbol regression tests and the existing UI suites.
6. Commit the tested site atomically against the latest remote head. Verify the exact successful Pages deployment. Sheets and GitHub are separate services: a pending or failed write is not a synchronized publication.

Suspended or unapproved assessments require quantity zero and null operative signal, stop and ceilings. Held classifications are protected. An execution-authorized ticket requires a separate explicitly reviewed workflow and currently fails closed here. All private snapshots, payloads and verification evidence must stay outside the public site.
