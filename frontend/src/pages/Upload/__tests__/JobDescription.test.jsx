import React from "react";
import { render, screen, waitFor, fireEvent } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import axios from "axios";
import JobDescription from "../JobDescription";
import { AuthProvider } from "../../../context/AuthContext";

//had to use fireEvent instead of the typical standard userEvent due to the fact that userEvent does a complete process and is extremely slow in completely 5000 character typing
//fireEvent directly does the chang, may look in the future for better solution or using userEvent in different way
//https://github.com/testing-library/user-event/discussions/977
//Adding timeout value to userEvent did not work up to 10 seconds so not worth using
jest.mock("axios");

describe("JobDescription Component", () => {
  beforeEach(() => {
    jest.clearAllMocks();
    //make sure the getItem doesnt overflow
    jest.spyOn(Storage.prototype, "getItem").mockClear();
  });

  it("renders existence check", () => {
    render(
      <AuthProvider>
        <JobDescription />
      </AuthProvider>,
    );
    expect(
      screen.getByPlaceholderText(/Enter job description here/i),
    ).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /upload/i })).toBeInTheDocument();
  });

  it("display character count and warn when approaching or exceeding the limit", () => {
    render(
      <AuthProvider>
        <JobDescription />
      </AuthProvider>,
    );
    const textArea = screen.getByPlaceholderText(/Enter job description here/i);

    // testing far away
    fireEvent.change(textArea, { target: { value: "j".repeat(3000) } });
    expect(screen.getByText(/3000 \/ 5000 characters/i)).toBeInTheDocument();
    expect(
      screen.queryByText(/You are almost at the character limit/i),
    ).not.toBeInTheDocument();
    expect(
      screen.queryByText(/Character limit exceeded/i),
    ).not.toBeInTheDocument();
    // test at/close
    fireEvent.change(textArea, { target: { value: "j".repeat(5000) } });
    expect(screen.getByText(/5000 \/ 5000 characters/i)).toBeInTheDocument();
    expect(
      screen.getByText(/You are almost at the character limit/i),
    ).toBeInTheDocument();
    // testing above limit
    fireEvent.change(textArea, { target: { value: "j".repeat(5001) } });
    expect(screen.getByText(/5001 \/ 5000 characters/i)).toBeInTheDocument();
    expect(screen.getByText(/Character limit exceeded/i)).toBeInTheDocument();
  });

  it("disable submit button and show error when character limit is exceeded", () => {
    render(
      <AuthProvider>
        <JobDescription />
      </AuthProvider>,
    );
    const textArea = screen.getByPlaceholderText(/Enter job description here/i);
    const submitButton = screen.getByRole("button", { name: /upload/i });

    //place characters
    fireEvent.change(textArea, { target: { value: "j".repeat(5001) } });
    expect(submitButton).toBeDisabled();
    expect(screen.getByText(/Character limit exceeded/i)).toBeInTheDocument();
  });

  it("display success text on successful call", async () => {
    //have to use Storage prototype and have it spy with to returning our fake token
    jest.spyOn(Storage.prototype, "getItem").mockImplementation((key) => {
      if (key === "token") return "idontlikethis";
      return null;
    });
    axios.post.mockResolvedValueOnce({ status: 200 });
    render(
      <AuthProvider>
        <JobDescription />
      </AuthProvider>,
    );

    const textArea = screen.getByPlaceholderText(/Enter job description here/i);
    const submitButton = screen.getByRole("button", { name: /upload/i });

    //placing valid one
    fireEvent.change(textArea, { target: { value: "valid".repeat(300) } });
    fireEvent.click(submitButton);

    expect(
      await screen.findByText(/Job description uploaded successfully!/),
    ).toBeInTheDocument();
    expect(axios.post).toHaveBeenCalledTimes(1);
    expect(axios.post).toHaveBeenCalledWith(
      "http://127.0.0.1:8000/api/job-description",
      { job_description: "valid".repeat(300) },
      {
        headers: {
          "Content-Type": "application/json",
          Authorization: "Bearer idontlikethis",
        },
      },
    );
  });

  it("display an error message on API fail", async () => {
    axios.post.mockRejectedValueOnce(new Error("API fail"));
    render(
      <AuthProvider>
        <JobDescription />
      </AuthProvider>,
    );

    const textArea = screen.getByPlaceholderText(/Enter job description here/i);
    const submitButton = screen.getByRole("button", { name: /upload/i });

    fireEvent.change(textArea, { target: { value: "Invalid desc" } });
    fireEvent.click(submitButton);

    expect(
      await screen.findByText(/An error occurred during submission./),
    ).toBeInTheDocument();
  });

  it("display an error message on not 200 API res", async () => {
    axios.post.mockResolvedValueOnce({ status: 400 });
    render(
      <AuthProvider>
        <JobDescription />
      </AuthProvider>,
    );

    const textArea = screen.getByPlaceholderText(/Enter job description here/i);
    const submitButton = screen.getByRole("button", { name: /upload/i });
    fireEvent.change(textArea, { target: { value: "400 response rip" } });
    fireEvent.click(submitButton);

    expect(
      await screen.findByText(/Failed to upload job description./),
    ).toBeInTheDocument();
  });

  it("disable submit button when text is empty", () => {
    render(
      <AuthProvider>
        <JobDescription />
      </AuthProvider>,
    );
    const submitButton = screen.getByRole("button", { name: /upload/i });
    expect(submitButton).toBeDisabled();
  });

  it("displays loading component while the job description upload is in progress", async () => {
    //set timeout for entire test
    jest.setTimeout(10000);

    // const mockResponse = {  status: 200 }; // give fake token to pass

    axios.post.mockImplementation(
      () =>
        new Promise((resolve) => {
          setTimeout(() => {
            resolve({
              status: 200,
            }); //make it sucess
          }, 1000); // give one second delay
        }),
    );
    // const user = userEvent.setup();

    render(
      <AuthProvider>
        <JobDescription />
      </AuthProvider>,
    );

    const textArea = screen.getByPlaceholderText(/Enter job description here/i);
    const submitButton = screen.getByRole("button", { name: /upload/i });

    //placing valid one
    fireEvent.change(textArea, { target: { value: "valid".repeat(300) } });
    fireEvent.click(submitButton);

    expect(screen.getByText("Loading...")).toBeInTheDocument(); // find loading to appear immedietely
    await waitFor(
      () => expect(screen.queryByText("Loading...")).not.toBeInTheDocument(),
      { timeout: 1500 },
    ); //WAIT for loading to stop after succeess
    expect(
      await screen.findByText(/Job description uploaded successfully!/),
    ).toBeInTheDocument();
  });
  it("display a custom error message - job description", async () => {
    // axios.post.mockRejectedValueOnce(new Error('API fail'));
    axios.post.mockRejectedValueOnce({
      response: {
        status: 400,
        data: { detail: "custom error" },
      },
    });
    render(<JobDescription />);

    const textArea = screen.getByPlaceholderText(/Enter job description here/i);
    const submitButton = screen.getByRole("button", { name: /upload/i });

    fireEvent.change(textArea, { target: { value: "Invalid desc" } });
    fireEvent.click(submitButton);

    expect(await screen.findByText("custom error")).toBeInTheDocument();
  });
});
