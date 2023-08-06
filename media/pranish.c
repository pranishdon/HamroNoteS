//vc= vs(1-e^(-t/RC))
#include<stdio.h>
#include<stdlib.h>
#include<math.h>

int main()
{
	float vs =10.0;
	float R=10000.0;
	float C=0.00008;
	float E=2.7182;
	float T=0;
	float dt=0.001;
	float VC=0.0;
	int i;

	FILE *fptr,*fptr2;
	fptr =fopen("data1.txt","w");
	fptr2=fopen("Data2.txt","w");
	fprintf(fptr,"itr\ttime(t)\tVC\n");

	for(i=1;i<=800;i++)
	{
		T=T+dt;
		VC= vs*(1-(pow(E,(-T/(R*C)))));

		fprintf(fptr,"%d  \t%.4f  \t%.4f\n",i,T,VC);
	}
	fprintf(fptr2,"itr\t Time \t  VC\n");

	double t1=0;

	for ( i=0;i<800;i++){
        t1+=dt;
       float discharge= vs*(pow(E,(-t1/(R*C))));
       fprintf(fptr2,"%d\t%1f \t%.4f\n",i,t1,discharge);

	}

	fclose(fptr2);

	fclose(fptr);
	return 0;


}
