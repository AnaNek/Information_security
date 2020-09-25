#include <stdio.h>
#include "license.h"

int main(void)
{
    int rc = check_license();
    
    if (rc == LICENSE_SUCCESS)
    {
    	printf("SUCCESS!!");
    }
    else
    {
    	printf("FAIL");
    }
    
    return 0;
}
