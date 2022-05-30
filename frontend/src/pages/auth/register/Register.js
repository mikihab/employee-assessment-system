import React, { Component } from "react";
import { Link, useHistory } from "react-router-dom";
import "./Register.css";
import Nav from "../../../components/auth/Nav";
import { setToken, fetchToken } from "../../../services/Auth";
import { useState } from "react";

import axios from "axios";
import {
  Flex,
  Box,
  FormControl,
  FormLabel,
  Input,
  InputGroup,
  HStack,
  InputRightElement,
  Stack,
  Button,
  Heading,
  Text,
  useColorModeValue,
} from "@chakra-ui/react";

function Register() {
  const handleShowClick = () => setShowPassword(!showPassword);
  const [showPassword, setShowPassword] = useState(false);
  const history = useHistory();
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [inst_id, setInst_id] = useState("");

  var bodyFormData = new FormData();
  const color = useColorModeValue("gray.50", "gray.800");
  const signIn = () => {
    history.push("/login");
  };

  const signupHandler = async (e) => {
    bodyFormData.append("username", email);
    bodyFormData.append("password", password);
    bodyFormData.append("name", name);
    bodyFormData.append("inst_id", inst_id);
    console.log(email);
    e.preventDefault();
    try {
      const response = await axios({
        method: "post",
        url: "http://127.0.0.1:8000/user",
        data: {
          name: name,
          email: email,
          password: password,
          inst_id: inst_id,
          is_master: "False",
        },
      }).then(function (response) {
        //handle success
        console.log(response);
        if (response.data.access_token) {
          setToken(response.data.access_token);
          Link("/user");
        }
      });
      setName("");
      setEmail("");
      setPassword("");
      setInst_id("");
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
          <Flex minH={"100vh"} align={"center"} justify={"center"} bg={color}>
            <Stack spacing={8} mx={"auto"} maxW={"lg"} py={12} px={6}>
              <Stack align={"center"}>
                <Heading fontSize={"4xl"} textAlign={"center"}>
                  Sign Up
                </Heading>
              </Stack>
              <Box rounded={"lg"} bg={color} boxShadow={"lg"} p={8}>
                <Stack spacing={4}>
                  <Box>
                    <FormControl id="name" isRequired>
                      <FormLabel>Name</FormLabel>
                      <Input
                        type="text"
                        onChange={(e) => setName(e.target.value)}
                      />
                    </FormControl>
                    <FormControl id="inst_id" isRequired>
                      <FormLabel>Institution Id</FormLabel>
                      <Input
                        type="number"
                        onChange={(e) => setInst_id(e.target.value)}
                      />
                    </FormControl>
                    <FormControl id="email" isRequired>
                      <FormLabel>Email address</FormLabel>
                      <Input
                        type="email"
                        onChange={(e) => setEmail(e.target.value)}
                      />
                    </FormControl>

                    <FormControl id="password" isRequired>
                      <FormLabel>Password</FormLabel>
                      <InputGroup>
                        <Input
                          type={showPassword ? "text" : "password"}
                          onChange={(e) => setPassword(e.target.value)}
                        />
                        <InputRightElement h={"full"}>
                          <Button variant={"ghost"} onClick={handleShowClick}>
                            {showPassword ? "Hide" : "Show"}
                          </Button>
                        </InputRightElement>
                      </InputGroup>
                    </FormControl>
                  </Box>
                  <Stack spacing={10} pt={2}>
                    <Button
                      loadingText="Submitting"
                      size="lg"
                      bg={"blue.400"}
                      color={"white"}
                      _hover={{
                        bg: "blue.500",
                      }}
                      onClick={signupHandler}
                    >
                      Sign up
                    </Button>
                  </Stack>
                  <Stack pt={6}>
                    <Text align={"center"}>
                      Already a user?{" "}
                      <Link color="teal.500" onClick={signIn}>
                        Sign In
                      </Link>
                    </Text>
                  </Stack>
                </Stack>
              </Box>
            </Stack>
          </Flex>
        </div>
      )}
    </>
  );
}
export default Register;
