#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include "license.h"

int get_serial_number(char *serial_number, int n)
{
    char *command = "";
    FILE *fp = NULL;
    char buf[128];
    char *ptr = serial_number;
	
    #if defined _WIN32 || defined __CYGWIN__
        //command = "wmic bios get serialnumber";
        command = "wmic csproduct get uuid";
    #elif __linux__
        command = "dmesg | grep UUID | grep \"Kernel\" | sed \"s/.*UUID=//g\" | sed \"s/\\ ro\\ quiet.*//g\"";
        // Вариант с мак адресом
        //command = "cat /sys/class/net/*/address";
    #elif TARGET_OS_MAC
        command = "system_profiler | grep Serial";
    #endif
	
    fp = popen(command, "r");
	
    if (fp == NULL) 
    {
        printf("Failed to run command\n" );
        return -1;
    }
    
    while (ptr) 
    {
        ptr = fgets(buf, sizeof(buf), fp);
        if (strcmp(buf, "\n") != 0)
        {
            strcpy(serial_number, buf);
        }
    }
    
    pclose(fp);
    return 0;
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

