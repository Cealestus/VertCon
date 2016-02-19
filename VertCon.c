//*****************************************************************************
//
// MSP432 main.c template - Empty main
//
//****************************************************************************

#include "msp.h"

volatile int counter;

void init(void){
	counter = 0;
}

void main(void)
{
	
    WDTCTL = WDTPW | WDTHOLD;           // Stop watchdog timer
    init();
    P2DIR |= (BIT7 | BIT6 | BIT4);
    P2OUT &= ~(BIT7 | BIT6 | BIT4);


    while(1){
    	int i;
    	if(counter == 2){
    		counter = 0;
    	} else{
    		counter++;
    	}
    	P2OUT &= ~(BIT7 | BIT6 | BIT4);
    	if(counter == 0){
    		P2OUT |= BIT4;
    	} else if(counter == 1){
    		P2OUT |= BIT6;
    	} else if(counter == 2){
    		P2OUT |= BIT7;
    	} else{

    	}
    	for(i=1000000; i>0; i--){         // Delay

    	}
    }
	
}
