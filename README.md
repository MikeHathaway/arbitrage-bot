# Arbitrage Bot

Automatically create CDP and lend it out on Compound when the stability fee is less than the prevailing interest rate for DAI in the Compound money market.

### Architecture

*MakerDao*
Chron job listening to MakerDAO Oracle and Compound Oracle -> Use pymaker to open CDP with allocated funds -> execute mint transaction on compound to generate cTokens -> profit 

Entry: pymaker: join -> open -> lock -> draw 
Exit: pymaker: wipe -> free -> exit

*Compound*
call mint method on CEther 

#### Research
- https://compound.finance/developers/api
- https://compound.finance/developers/ctokens
- https://github.com/makerdao/pymaker
- https://github.com/makerdao/sai
