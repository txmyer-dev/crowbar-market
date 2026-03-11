# InvoiceExtract Workflow

Extracts structured data from PDF invoices for import into hledger or review. Uses a deterministic extraction approach with fallback chain.

## When to Use

- User has a PDF invoice and wants structured data extracted
- User says "extract invoice", "parse this invoice", "what's on this invoice"
- Preparing invoice data for hledger import

## Input

PDF invoice file (path provided by user). Can be:
- Digital PDF (text-selectable)
- Scanned PDF (image-based, requires OCR)
- Multi-page invoice

## Extraction Schema

Extract the following fields into structured JSON:

```json
{
  "vendor": {
    "name": "Company Name",
    "address": "Full address if present",
    "tax_id": "EIN/VAT if present"
  },
  "invoice_number": "INV-2026-001",
  "date": "2026-03-01",
  "due_date": "2026-03-31",
  "currency": "USD",
  "line_items": [
    {
      "description": "Monthly hosting - Pro plan",
      "quantity": 1,
      "unit_price": 49.00,
      "amount": 49.00
    }
  ],
  "subtotal": 49.00,
  "tax": [
    {
      "description": "Sales Tax (8.25%)",
      "amount": 4.04
    }
  ],
  "total": 53.04,
  "payment_method": "Credit card ending in 4242",
  "notes": "Any additional notes on the invoice"
}
```

**Optional fields** (include if present, omit if not): `vendor.address`, `vendor.tax_id`, `due_date`, `payment_method`, `notes`

## Extraction Approach — Fallback Chain

### Tier 1: Text Extraction (Try First)

Use the Documents skill or Read tool to extract text from the PDF. For digital PDFs, this gives clean text.

Parse the extracted text using these patterns:

**Date formats** (support all of these):
- `2026-03-01`, `03/01/2026`, `03/01/26`
- `March 1, 2026`, `Mar 1, 2026`, `1 March 2026`
- `01-Mar-2026`, `01.03.2026`

**Currency detection:**
- Symbol: `$`, `€`, `£`, `¥`, `CA$`, `A$`
- ISO code: `USD`, `EUR`, `GBP`, `JPY`, `CAD`, `AUD`
- Default to USD if no currency indicator found

**Amount patterns:**
- `$1,234.56`, `1234.56`, `$1234`, `1.234,56` (European)

### Tier 2: OCR Fallback (If Text Extraction Fails)

If the PDF has no selectable text (scanned document), inform the user:

> "This appears to be a scanned invoice. I can extract what I can see from the document, but accuracy may be lower. Want me to proceed?"

Use the Read tool to view the PDF as an image and extract data visually.

### Tier 3: Manual Entry Assist

If extraction confidence is low, present what was found and ask the user to fill gaps:

> "I extracted most fields but couldn't confidently identify the tax amount. Here's what I have — can you confirm or fill in the missing fields?"

## Validation Rules

After extraction, verify:

1. **Math check:** `total` should equal `subtotal + sum(tax amounts)` within $0.02 tolerance
2. **Date check:** `date` should be a valid date, `due_date` should be after `date`
3. **Line items check:** `sum(line_item amounts)` should equal `subtotal` within $0.02
4. **Currency check:** All amounts use the same currency

If validation fails, flag the discrepancy:
```markdown
⚠️ Validation Warning: Line items sum to $48.00 but subtotal shows $49.00. Difference: $1.00.
```

## Output Format

Present two outputs:

### 1. Structured JSON (for programmatic use)
The JSON schema above, populated with extracted data.

### 2. Human-Readable Summary
```markdown
## Invoice Summary

| Field | Value |
|-------|-------|
| **Vendor** | Company Name |
| **Invoice #** | INV-2026-001 |
| **Date** | March 1, 2026 |
| **Due Date** | March 31, 2026 |
| **Currency** | USD |

### Line Items

| Description | Qty | Unit Price | Amount |
|-------------|-----|-----------|--------|
| Monthly hosting - Pro plan | 1 | $49.00 | $49.00 |

| | |
|---|---|
| **Subtotal** | $49.00 |
| **Tax (8.25%)** | $4.04 |
| **Total** | **$53.04** |

✅ Validation passed — all totals reconcile.
```

### 3. hledger Transaction (Optional — If User Wants Import)

If the user wants to import into hledger, generate the transaction:

```hledger
2026-03-01 Company Name | INV-2026-001
    expenses:hosting          $49.00
    expenses:tax:sales         $4.04
    liabilities:credit-card  $-53.04
```

Ask which expense account to use if uncertain. Reference existing account names from the journal.

## Quality Check

Before delivering:
- [ ] All required fields are populated (vendor name, date, at least one line item, total)
- [ ] Math validation passed (or discrepancies flagged)
- [ ] Currency is correctly identified
- [ ] Date format is ISO 8601 in JSON output
- [ ] Optional fields are omitted (not null) if not present on invoice
- [ ] hledger transaction uses correct account names from existing journal
