# Weak-to-strong crypto prompt examples

## Token DD
Weak: `is this token legit?`
Strong: `Review <TOKEN> on <CHAIN>. Return: what it is, legitimacy questions, liquidity questions, concentration risks, red flags, and 3 next checks. Separate facts from assumptions.`

## Wallet review
Weak: `what is this wallet doing?`
Strong: `Analyze wallet <ADDRESS> on <CHAIN>. Return: balance picture, transfer behavior, protocol exposure, suspicious signs, and next checks. Keep claims tied to observable behavior.`

## Yield scan
Weak: `find high yield`
Strong: `Scan <CHAIN OR NICHE> for yield options relevant to <CAPITAL SIZE> and <RISK PROFILE>. Return: candidates, yield source, TVL/liquidity questions, risks, and what to verify. Do not rank by APY alone.`
