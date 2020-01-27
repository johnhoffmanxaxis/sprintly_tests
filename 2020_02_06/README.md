# AOC 2019/day/6

https://adventofcode.com/2019/day/6

*Requires python 3.8*

### Usage:

```
python orbit.py <orbit_map.txt> [<obj1> <obj2>]

```

Where `<orbit_map.txt>` is the path to the text file with a format of

```
COM)A
A)B
...
```

that enumerates all of the orbits in the universe.

Optionally, you can find the path between `obj1` and `obj2` by including them as two extra command line args.

The output looks something like this:

```
(py38) john.hoffman@NYCGRMJHOFFMAC:2020_02_06$ python orbit.py full_input.txt YOU SAN
Total orbit count: 142915
Finding path between YOU and SAN
YOU->R85->LC3->RSW->6NZ->F6R->6ZJ->8FV->9YW->N2V->N9H->SRY->Q4N->47R->VKY->G4G->L4D->5H8->NCP->T6Q->3SN->4YF->VR9->JMT->6JS->9LZ->954->SF1->96R->XX1->76V->3L5->1V2->17H->VJS->2GN->YFR->8R2->D95->7TT->F5Y->VRB->JWK->CZ7->SL3->25F->HHL->D1M->R57->KSJ->HT2->N4X->NX9->MVZ->FYX->WSX->ZW3->RX2->ZLY->G31->K4X->NYV->2WR->GW7->D81->8JB->9CY->NP3->69L->X5P->FZB->16B->DB7->RGD->PX7->GQZ->5KM->65Z->S1R->TMG->6L7->RD7->X9M->XKV->W73->8WL->ZX9->PR3->J9S->2NJ->93Q->XMQ->YY9->FTV->PM5->PZN->G97->2GS->C6T->13V->YD6->S6M->8LW->ZKR->GH2->94D->C7Q->Y9T->QG3->BTX->2V2->PMD->RJN->2SK->3FD->GT8->YLM->8TK->H1G->VF8->XDB->3Q7->55S->JKC->5MQ->Z81->P2N->4NH->GWV->D1C->QH5->DZP->G8G->SNJ->FKN->QJ8->3X7->425->PRT->BQ4->VBT->NXK->JS9->LWH->TVG->WTG->JL8->1YR->XK2->FPJ->NJ4->6DD->PCK->K67->NLG->78Z->RHH->JJ4->RNP->T12->J86->MHT->2V7->Y86->ZYW->RT3->JZF->G55->XZP->6BS->TYQ->LTW->2VW->RMH->K36->6C8->4CP->X9R->FK9->B69->F4N->RHQ->R6X->MQM->6R2->CK2->FRV->F1Y->QFX->TJF->LLK->HGB->GLZ->ZWC->YKV->CY8->JF2->L81->8G6->Q96->4XF->6W2->PM7->PW8->TVQ->8PV->9LW->RBB->XPL->YNP->832->WHL->HZ4->1HH->2R9->BCQ->CZY->JF6->1CR->3L1->DNH->9JD->Z3X->XK9->SPT->2B8->JXQ->QCJ->FSY->D18->G26->3VT->JQC->THH->56B->FWB->KBL->924->88G->H5X->83Q->YHF->Q2G->GZW->61P->6J7->QBW->HP7->8V7->Q73->PZV->7D1->SYP->NX2->6NB->PFL->RZD->2VP->V18->8P6->XFC->KYD->GHV->3L7->X1C->1S5->5BR->S46->G5F->ML7->DVZ->G9Q->V2B->98Z->TZX->8VC->9X7->86K->X58->5ZG->2JJ->6GY->DTT->LHX->YNY->SAN
Path length: 286
```

The first number is the answer to part 1. The `Path length` output is the answer to part 2, except part two asks the total path length between the orbits *in between* `YOU` and `SAN`, which is the output number `286` *minus 3*
