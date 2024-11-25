import React from 'react';
import { render, screen,fireEvent, waitFor} from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import axios from 'axios';
import FileUpload from '../FileUpload'; 
import { AuthProvider } from '../../../context/AuthContext';
//tests created for task 9/10

jest.mock('axios');
describe('FileUpload Component', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('display an error for not pdf file upload', async () => {
    render(<AuthProvider><FileUpload /></AuthProvider>);
    const fileInput = screen.getByLabelText('Upload File');
    const invalidFile = new File(['content'], 'safnoor.txt', { type: 'text/plain' });
    await userEvent.upload(fileInput, invalidFile);
    expect(await screen.findByText(/File must be a PDF/)).toBeInTheDocument();
  });

  it('display error for file over 2MB', async () => {
    render(<AuthProvider><FileUpload /></AuthProvider>);
    const fileInput = screen.getByLabelText('Upload File');

    //using blob and specfic arry to create over limit
    //https://stackoverflow.com/questions/25001677/how-to-generate-a-binary-blob-object-in-java-of-a-specific-size
    //https://stackoverflow.com/questions/61763575/how-to-mock-a-file-with-a-big-size-in-javascript-for-testing-purposes
    const largeFile = new File([new Blob([new Uint8Array(2 * 1024 * 1024 + 1)])], 'largesafnoor.pdf', {
      type: 'application/pdf',
    });

    await userEvent.upload(fileInput, largeFile);
    expect(await screen.findByText(/File size must be under 2 MB/)).toBeInTheDocument();
  });

  it('enable upload button for valid PDF file', async () => {
    render(<AuthProvider><FileUpload /></AuthProvider>);
    const fileInput = screen.getByLabelText('Upload File');
    const validFile = new File(['content'], 'safnoor.pdf', { type: 'application/pdf' });

    await userEvent.upload(fileInput, validFile);
    const uploadButton = screen.getByRole('button', { name: /upload/i });
    expect(uploadButton).not.toBeDisabled();
  });

  it('display a success message on successful file upload', async () => {
    axios.post.mockResolvedValueOnce({ status: 200 });
    render(<AuthProvider><FileUpload /></AuthProvider>);

    const fileInput = screen.getByLabelText('Upload File');
    const validFile = new File(['content'], 'safnoor.pdf', { type: 'application/pdf' });
    await userEvent.upload(fileInput, validFile);
    const uploadButton = screen.getByRole('button', { name: /upload/i });
    await userEvent.click(uploadButton);

    expect(await screen.findByText(/File uploaded successfully!/)).toBeInTheDocument();
    expect(axios.post).toHaveBeenCalledTimes(1);
  });
  

  it('display an error message on API fail', async () => {
    axios.post.mockRejectedValueOnce(new Error('API fail'));
    render(<AuthProvider><FileUpload /></AuthProvider>);

    const fileInput = screen.getByLabelText('Upload File');
    const validFile = new File(['content'], 'safnoor.pdf', { type: 'application/pdf' });
    await userEvent.upload(fileInput, validFile);
    const uploadButton = screen.getByRole('button', { name: /upload/i });
    await userEvent.click(uploadButton);

    expect(await screen.findByText(/An error occurred during file upload./)).toBeInTheDocument();
  });

  it('handle non 200 status code', async () => {
    axios.post.mockResolvedValueOnce({ status: 400 });
    render(<AuthProvider><FileUpload /></AuthProvider>);

    const fileInput = screen.getByLabelText('Upload File');
    const validFile = new File(['content'], 'valid.pdf', { type: 'application/pdf' });
    await userEvent.upload(fileInput, validFile);
    const uploadButton = screen.getByRole('button', { name: /upload/i });
    await userEvent.click(uploadButton);

    expect(await screen.findByText(/Failed to upload the file./)).toBeInTheDocument();
  });

  it('displays loading component while the file upload is in progress', async () => {
    //set timeout for entire test 
    jest.setTimeout(10000);

    // const mockResponse = {  status: 200 }; // give fake token to pass

    axios.post.mockImplementation(() =>
      new Promise((resolve) => {
        setTimeout(() => {
          resolve({
            status: 200
          }); //make it sucess
        }, 1000); // give one second delay
      })
    );

    render(<AuthProvider><FileUpload /></AuthProvider>);
    const user = userEvent.setup();

    const fileInput = screen.getByLabelText('Upload File');
    const validFile = new File(['content'], 'safnoor.pdf', { type: 'application/pdf' });
    await userEvent.upload(fileInput, validFile);
    const uploadButton = screen.getByRole('button', { name: /upload/i });
    // await userEvent.click(uploadButton);
    fireEvent.click(uploadButton); //trigger with fireEvent so no delay i dont want full process

    expect(screen.getByText('Loading...')).toBeInTheDocument(); // find loading to appear immedietely 

    await waitFor(() => expect(screen.queryByText('Loading...')).not.toBeInTheDocument(), { timeout: 1500 }); //WAIT for loading to stop after succeess
    expect(await screen.findByText(/File uploaded successfully!/)).toBeInTheDocument();

  });
  it('display a custom error message file upload', async () => {
    // axios.post.mockRejectedValueOnce(new Error('API fail'));
    axios.post.mockRejectedValueOnce({
      response: {
        status: 400,
        data: { detail: 'custom error' },
      },
    });

    render(<FileUpload />);

    const fileInput = screen.getByLabelText('Upload File');
    const validFile = new File(['content'], 'safnoor.pdf', { type: 'application/pdf' });
    await userEvent.upload(fileInput, validFile);
    const uploadButton = screen.getByRole('button', { name: /upload/i });
    await userEvent.click(uploadButton);

    expect(await screen.findByText("custom error")).toBeInTheDocument();
  });
});
