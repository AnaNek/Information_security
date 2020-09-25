#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include "license.h"

int split(char *serial_number, int n)
{
    int i;
	for (i = 0; i < n && serial_number[i] != ':'; i++)
	{ }
	
	memmove(serial_number, serial_number + i + 1, n - i);
	return 0;
}

int get_serial_number(char *serial_number, int n)
{
	char *command = "";
	FILE *fp = NULL;
	
	#ifdef _WIN32
	    command = "wmic bios get serialnumber";
	#elif __linux__
	    command = "dmidecode -t system | grep Serial";
	#elif __unix__
	    command = "system_profiler | grep Serial";
	#endif
	
	fp = popen(command, "r");
	
	if (fp == NULL) 
	{
		printf("Failed to run command\n" );
    	return -1;
    }
    
    if (fgets(serial_number, n, fp) != NULL) 
    {
        split(serial_number, n);
    	pclose(fp);
	    return 0;
    }
  
	pclose(fp);
	return -1;
}

int write_license(void)
{
    FILE *license = NULL;
    int n = 128;
    char sn[n];
    
    int rc = get_serial_number(sn, n);
    
	license = fopen("license", "w");
	fprintf(license, "%s", sn);
	fclose(license);
	
	return 0;
}

int check_license(void)
{
	FILE *license = NULL;
	int n = 128;
    char correct_sn[n];
    char sn[n];
    
	license = fopen("license", "r");
	if (license == NULL)
	{
		return LICENSE_FAIL;
	}
	fgets(correct_sn, n, license);
	
	int rc = get_serial_number(sn, n);
	
	if (strcmp(sn, correct_sn) != 0)
	{
	    fclose(license);
		return LICENSE_FAIL;
	}
	
	fclose(license);
	return LICENSE_SUCCESS;
}
