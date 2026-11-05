// Append-only documented follow-ups. Original reports and source packages are unchanged.
window.FP_ENTRY_PLAN_FOLLOWUPS={
  "schema": "fp.entry-plan-followups.v1",
  "records": [
    {
      "schema": "fp.entry-plan-followup.v1",
      "id": "CTSH-20261105-B-V2-OPEN-REVIEW-1",
      "planId": "CTSH-20261105-B-V2",
      "reportId": "A278",
      "version": "PUBLIC_FINAL_V2",
      "sourcePlan": {
        "schema": "fp.entry-plan.v1",
        "id": "CTSH-20261105-B-V2",
        "ticker": "CTSH",
        "version": "PUBLIC_FINAL_V2",
        "reportId": "A278",
        "predecessorReportId": "A268",
        "proposedAt": "2026-11-05T11:42:18.149077Z",
        "expiresAt": "2026-11-05T16:00:00-05:00",
        "executionSuspended": true,
        "events": [
          {
            "state": "pending",
            "at": "2026-11-05T11:42:18.149077Z",
            "evidenceEs": "Fuente PUBLIC_FINAL_V2, publication_metadata.json: sin señal actual, entrada aprobada, orden ni ejecución. Registro inicial; no prueba de activación.",
            "evidenceEn": "Source PUBLIC_FINAL_V2, publication_metadata.json: no current signal, approved entry, order or execution. Initial record; no activation evidence.",
            "source": "research/2026-11-05/CTSH-stage35-B-V2/publication_metadata.json"
          }
        ],
        "strategy": "FundamentalPullback · Stage 3.5 B",
        "route": "B",
        "date": "2026-11-05",
        "currency": "USD",
        "signal": {
          "closeGt": 65.26,
          "closeLte": 65.78,
          "eligibleCloses": "09:45–15:45 EST"
        },
        "levels": {
          "cap": 65.78,
          "M": 61.55,
          "S": 61.2
        }
      },
      "sourceLibrary": {
        "path": "data/lib-ctsh-prospective.js",
        "sha256": "c374ef6b1649ffd311d658092eadc08bfefe89f2a033ab64ee319a2f4e40f76e"
      },
      "sourcePackage": {
        "path": "research/2026-11-05/CTSH-stage35-B-V2/CTSH_Stage35_B_20261105_PUBLIC_FINAL_V2.zip",
        "sha256": "e46c290a53863b24cb058303fa1b9c42bc46578cde13e3e94e76edd62c744773"
      },
      "predecessor": {
        "state": "pending",
        "at": "2026-11-05T11:42:18.149077Z",
        "evidenceEs": "Fuente PUBLIC_FINAL_V2, publication_metadata.json: sin señal actual, entrada aprobada, orden ni ejecución. Registro inicial; no prueba de activación.",
        "evidenceEn": "Source PUBLIC_FINAL_V2, publication_metadata.json: no current signal, approved entry, order or execution. Initial record; no activation evidence.",
        "source": "research/2026-11-05/CTSH-stage35-B-V2/publication_metadata.json"
      },
      "state": "suspended",
      "at": "2026-11-05T14:54:51.319837+00:00",
      "observedReviewAt": "2026-11-05T14:49:13.130989+00:00",
      "requestsStartedAt": "2026-11-05T14:46:31+00:00",
      "barOpenedAt": "2026-11-05T09:30:00-05:00",
      "barClosedAt": "2026-11-05T09:45:00-05:00",
      "evidenceEs": "El cierre de la primera vela de quince minutos fue 66,5975 USD, fuera de (65,26; 65,78], y el máximo regular 67,8572 superó 66,50. No hubo señal de entrada según B V2. Volver a la banda requiere revisión registrada, no una valoración completa nueva ni una espera fija. No se declara reactivación, operación ni cambio de A268.",
      "evidenceEn": "The first fifteen-minute bar closed at USD 66.5975, outside (65.26, 65.78], and its regular-session high of 67.8572 exceeded 66.50. B V2 did not produce an entry signal. Returning to the band requires a recorded review, not a new full valuation or a fixed waiting period. No reactivation, trade or change to A268 is declared.",
      "source": {
        "path": "research/2026-11-05/CTSH-stage35-B-V2-opening-review/event_record.json",
        "sha256": "6364e8671c2f5ff5da2b56f14ce6d40cd9dc88aa9f36e3617fbd8dd9ccb70303"
      },
      "reader": {
        "path": "research/2026-11-05/CTSH-stage35-B-V2-opening-review/index.html",
        "sha256": "35c50f225bab1d30e7af523774321803c46b166421f136618571d62acb16ab62"
      },
      "archive": {
        "path": "research/2026-11-05/CTSH-stage35-B-V2-opening-review/CTSH_B_V2_Opening_Review_20261105_PUBLIC_FINAL.zip",
        "sha256": "e3ca148cc17b42e681873ef5f91ffdcc26b371bf37999751e808f1e165a1a047"
      }
    }
  ]
};
