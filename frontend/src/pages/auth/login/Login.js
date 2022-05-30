import React, { useState } from "react";
//import "./login.css";
import auth from "../../../services/AuthServices";
import { setToken, fetchToken } from "../../../services/Auth";
import Nav from "../../../components/auth/Nav";

import { Link, NavLink, useHistory } from "react-router-dom";
import {
  Flex,
  Heading,
  Input,
  Button,
  InputGroup,
  Stack,
  InputLeftElement,
  chakra,
  Box,
  Avatar,
  FormControl,
  FormHelperText,
  InputRightElement,
} from "@chakra-ui/react";

function Login(props) {
  const [showPassword, setShowPassword] = useState(false);
  const history = useHistory();
  const handleClick = () => {
    history.push("/path/to/push");
  };
  const handleShowClick = () => setShowPassword(!showPassword);
  const [isLoggedIn, setisLoggedIn] = useState(false);
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  var bodyFormData = new FormData();
  const signUp = () => {
    history.push("/register");
  };

  const handleSubmit = async (e) => {
    bodyFormData.append("username", username);
    bodyFormData.append("password", password);
    e.preventDefault();
    try {
      auth
        .LoginAuth(username, password)
        .then((response) => {
          console.log(response.data.access_token);
          if (response.data) {
            //props.login(response.data.user);
            setToken(response.data.acess_token);

            console.log(isLoggedIn);
            console.log(response.data.user);
            console.log(fetchToken);

            history.push("/dashboard/teacher");
          } else {
          }
        })
        .catch((error) => {
          console.log(error);
        });
      setisLoggedIn(true);
    } catch (err) {}
  };

  return (
    <>
      {fetchToken() ? (
        fetchToken() ? (
          history.push("/dashboard/teacher")
        ) : (
          history.push("/dashboard/teacher")
        )
      ) : (
        <div>
          <Nav></Nav>
          <Flex
            flexDirection="column"
            width="100wh"
            height="100vh"
            backgroundColor="gray.200"
            justifyContent="center"
            alignItems="center"
          >
            <Stack
              flexDir="column"
              mb="2"
              justifyContent="center"
              alignItems="center"
            >
              <Avatar bg="teal.500" />
              <Heading color="teal.400">Employee Assessment System</Heading>
              <Box minW={{ base: "90%", md: "468px" }}>
                <form>
                  <Stack
                    spacing={4}
                    p="1rem"
                    backgroundColor="whiteAlpha.900"
                    boxShadow="md"
                  >
                    <FormControl>
                      <InputGroup>
                        <InputLeftElement pointerEvents="none" />
                        <Input
                          type="email"
                          placeholder="email address"
                          onChange={(e) => setUsername(e.target.value)}
                        />
                      </InputGroup>
                    </FormControl>
                    <FormControl>
                      <InputGroup>
                        <InputLeftElement
                          pointerEvents="none"
                          color="gray.300"
                        />
                        <Input
                          type={showPassword ? "text" : "password"}
                          placeholder="Password"
                          onChange={(e) => setPassword(e.target.value)}
                        />
                        <InputRightElement width="4.5rem">
                          <Button
                            h="1.75rem"
                            size="sm"
                            onClick={handleShowClick}
                          >
                            {showPassword ? "Hide" : "Show"}
                          </Button>
                        </InputRightElement>
                      </InputGroup>
                      <FormHelperText textAlign="right">
                        <Link>forgot password?</Link>
                      </FormHelperText>
                    </FormControl>
                    <Button
                      borderRadius={0}
                      type="submit"
                      variant="solid"
                      colorScheme="teal"
                      width="full"
                      onClick={handleSubmit}
                    >
                      Login
                    </Button>
                  </Stack>
                </form>
              </Box>
            </Stack>

            <Box>
              New User?{" "}
              <Link color="teal.500" onClick={signUp}>
                Sign Up
              </Link>
            </Box>
          </Flex>
        </div>
      )}
    </>
  );
}

export default Login;
