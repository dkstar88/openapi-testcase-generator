# Openapi-Testcase-Generator
Generates testcases from openapi spec, automates the boring part of the testcase development

```shell
python import-swagger.py --url=https://petstore.swagger.io/v2/swagger.json
```

This will generate one feature for one endpoint. Below is an example of `deleteOrder.feature`

```
@api @store
Feature: Delete purchase order by ID
    For valid response try integer IDs with positive integer value. Negative or non-integer values will generate API errors
    

    Scenario: deleteOrder return Invalid ID supplied
        # delete - /store/order/{orderId}
        Given a request url /store/order/1
        When the request sends delete
        Then the response status is 400
    

    Scenario: deleteOrder return Order not found
        # delete - /store/order/{orderId}
        Given a request url /store/order/1
        When the request sends delete
        Then the response status is 404
    
```