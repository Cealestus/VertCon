//*****************************************************************************
//
// MSP432 main.c template - Empty main
//
//****************************************************************************

#include "msp.h"
#include "driverlib.h"

volatile int counter;

void init(void){
	counter = 0;
}

void check_light(void){
	if(GPIO_INPUT_PIN_LOW == GPIO_getInputPinValue(GPIO_PORT_P1, GPIO_PIN5)){
		P2OUT |= BIT7;
	}
	else{
		P2OUT &= ~BIT7;
	}

}
void main(void)
{
	
    WDTCTL = WDTPW | WDTHOLD;           // Stop watchdog timer
    init();
    GPIO_setAsOutputPin(GPIO_PORT_P2,GPIO_PIN7);
    GPIO_setAsOutputPin(GPIO_PORT_P2,GPIO_PIN6);
	GPIO_setAsOutputPin(GPIO_PORT_P2,GPIO_PIN4);
	GPIO_setAsInputPin(GPIO_PORT_P1,GPIO_PIN5);

    while(1){
    	int i;
    	if(counter == 1){
    		counter = 0;
    	} else{
    		counter++;
    	}

    	if(counter == 0){
    		P2OUT &= ~(BIT6);
    		P2OUT |= BIT4;
        	check_light();

    	}
    	else if(counter == 1){
    		P2OUT &= ~(BIT4);
    		P2OUT |= BIT6;
        	check_light();

    	} else{

    	}
    	for(i=1000000; i>0; i--);         // Delay
    }
	
}
