#include <stdio.h>
#include "license.h"

int main(void)
{
    int rc = check_license();
    
    if (rc == LICENSE_SUCCESS)
    {
    	printf("SUCCESS! You have permission\n");
    }
    else
    {
    	printf("FAIL. You need to run installer first\n");
    }
    
    return 0;
}
