#include <stdio.h>

int main()
{
int x ;
int t$1 ;
int y ;
int α ;
int β ;
int ι1 ;
int t$2 ;
int t$3 ;
int τ ;
int t$4 ;
int ι2 ;
int π ;
int t$5 ;
int t$6 ;
int t$7 ;

L1: 
L2: t$1=x*2;
L3: y=t$1;
L4: α=0;
L5: β=1;
L6: ι1=0;
L7: printf("%d\n",ι1);
L8: t$2=ι1+1;
L9: ι1=t$2;
L10: if (ι1 < 1) goto L12;
L11: goto L21;
L12: printf("%d\n",ι1);
L13: t$3=α+β;
L14: τ=t$3;
L15: α=β;
L16: β=τ;
L17: t$4=ι1+1;
L18: ι1=t$4;
L19: printf("%d\n",α);
L20: goto L10;
L21: ι2=0;
L22: π=1;
L23: t$5=ι2+1;
L24: ι2=t$5;
L25: t$6=π*ι2;
L26: π=t$6;
L27: printf("%d\n",π);
L28: if (ι2 >= 7) goto L30;
L29: goto L23;
L30: x=6;
L31: // par, x, _, CV
L32: // par, t$7, _, RET
L33: // call, διπλάσιο, _, _
L34: τ=t$7;
L35: printf("%d\n",τ);
L36: 
L37: 
}

