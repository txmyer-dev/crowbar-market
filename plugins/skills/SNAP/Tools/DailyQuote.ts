#!/usr/bin/env bun
/**
 * DailyQuote.ts - Serve a random Alex Hormozi quote at session start
 *
 * Reads the consolidated quotes file from SecondBrain and outputs
 * a random quote. Called by StartupGreeting.hook.ts.
 *
 * Exports: Quote interface, parseQuote(), loadAllQuotes(), pickRandomQuote()
 * for use by DailyWallpaper.ts and other consumers.
 *
 * Output (standalone): A formatted quote string to stdout
 */

import { readFileSync } from 'fs';
import { join } from 'path';

export interface Quote {
  text: string;
  attribution: string;
  raw: string;
}

const FALLBACK_QUOTES = [
  '"Discipline Equals Freedom." -- Alex Hormozi',
  '"You have nothing to lose and that makes you a very dangerous person." -- Alex Hormozi',
  '"This is what hard feels like. And this is why most people can\'t do it. But you can." -- Alex Hormozi',
  '"Successful people see opportunity in every failure normal people see failure in every opportunity." -- Alex Hormozi',
  '"Until you win, effort always goes unnoticed. Get used to it." -- Alex Hormozi',
  '"The world belongs to those who can continue to work without seeing the result of their work." -- Alex Hormozi',
  '"Everything worth doing is hard, and the more worth doing it is, the harder it is." -- Alex Hormozi',
  '"I don\'t have to deserve success. I can still just do the stuff that gets it." -- Alex Hormozi',
  '"Shame only exists in the shadows. Once you put it in the light you look at it and it evaporates." -- Alex Hormozi',
  '"I will never wish for fewer epic stories at the end of my life." -- Alex Hormozi',
];

/**
 * Parse a raw quote line like `"quote text" -- Attribution` into parts.
 */
export function parseQuote(raw: string): Quote {
  const dashMatch = raw.match(/^"(.+)"\s*--\s*(.+)$/s);
  if (dashMatch) {
    return { text: dashMatch[1].trim(), attribution: dashMatch[2].trim(), raw };
  }
  // Fallback: treat entire string as text, no attribution
  return { text: raw.replace(/^"|"$/g, ''), attribution: '', raw };
}

/**
 * Load all quotes from the SecondBrain quotes file.
 * Falls back to embedded quotes if file is missing or empty.
 */
export function loadAllQuotes(): Quote[] {
  const quotesPath = join(
    process.env.HOME || process.env.USERPROFILE || '',
    'My Drive/SecondBrain/Knowledge/Alex-Hormozi-Quotes.md'
  );

  try {
    const content = readFileSync(quotesPath, 'utf-8');
    const rawQuotes = content
      .split('\n')
      .filter(line => line.startsWith('- "') && line.includes(' -- '))
      .map(line => line.slice(2).trim());

    if (rawQuotes.length === 0) {
      return FALLBACK_QUOTES.map(q => parseQuote(q));
    }
    return rawQuotes.map(q => parseQuote(q));
  } catch {
    return FALLBACK_QUOTES.map(q => parseQuote(q));
  }
}

/**
 * Pick a random quote from all available quotes.
 */
export function pickRandomQuote(): Quote {
  const quotes = loadAllQuotes();
  return quotes[Math.floor(Math.random() * quotes.length)];
}

// Standalone mode: output a random quote to stdout
if (import.meta.main) {
  const quote = pickRandomQuote();
  console.log(quote.raw);
}
