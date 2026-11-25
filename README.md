# Example Voting App

A simple distributed application running across multiple Docker containers.

## devops ci pipeline

                    DEVELOPER PUSH / PULL REQUEST
                                |
                                v
                         CHECKOUT SOURCE
                                |
                                v
                    PREPARE CI ENVIRONMENT
                                |
                 +--------------+--------------+
                 |              |              |
                 v              v              v
             VOTE SERVICE   RESULT SERVICE   WORKER SERVICE
                 |              |              |
              Lint           Lint           Lint
                 |              |              |
            Unit Tests      Unit Tests      Unit Tests
                 |              |              |
                 +--------------+--------------+
                                |
                                v
                      BUILD DOCKER IMAGES
                                |
                                v
                   START DOCKER COMPOSE TEST ENV
                                |
                                v
                    WAIT FOR SERVICE HEALTH
                                |
                                v
                          SMOKE TESTS
                                |
                                v
                       INTEGRATION TESTS
                                |
                                v
                         E2E TESTS
                                |
                                v
                    STOP TEST ENVIRONMENT
                                |
                                v
                     TAG IMAGES WITH GIT SHA
                                |
                                v
                    PUBLISH IMAGES TO REGISTRY
                                |
                                v
                         CI SUCCESS

