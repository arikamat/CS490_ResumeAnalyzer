import React from 'react';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import axios from 'axios';
import FileUpload from '../FileUpload'; 

//tests created for task 9/10

jest.mock('axios');
describe('FileUpload Component', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('display an error for not pdf file upload', async () => {
    render(<FileUpload />);
    const fileInput = screen.getByLabelText('Upload File');
    const invalidFile = new File(['content'], 'safnoor.txt', { type: 'text/plain' });
    await userEvent.upload(fileInput, invalidFile);
    expect(await screen.findByText(/File must be a PDF/)).toBeInTheDocument();
  });

  it('display error for file over 2MB', async () => {
    render(<FileUpload />);
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
    render(<FileUpload />);
    const fileInput = screen.getByLabelText('Upload File');
    const validFile = new File(['content'], 'safnoor.pdf', { type: 'application/pdf' });

    await userEvent.upload(fileInput, validFile);
    const uploadButton = screen.getByRole('button', { name: /upload/i });
    expect(uploadButton).not.toBeDisabled();
  });

  it('display a success message on successful file upload', async () => {
    axios.post.mockResolvedValueOnce({ status: 200 });
    render(<FileUpload />);

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
    render(<FileUpload />);

    const fileInput = screen.getByLabelText('Upload File');
    const validFile = new File(['content'], 'safnoor.pdf', { type: 'application/pdf' });
    await userEvent.upload(fileInput, validFile);
    const uploadButton = screen.getByRole('button', { name: /upload/i });
    await userEvent.click(uploadButton);

    expect(await screen.findByText(/An error occurred during file upload./)).toBeInTheDocument();
  });

  it('handle non 200 status code', async () => {
    axios.post.mockResolvedValueOnce({ status: 400 });
    render(<FileUpload />);

    const fileInput = screen.getByLabelText('Upload File');
    const validFile = new File(['content'], 'valid.pdf', { type: 'application/pdf' });
    await userEvent.upload(fileInput, validFile);
    const uploadButton = screen.getByRole('button', { name: /upload/i });
    await userEvent.click(uploadButton);

    expect(await screen.findByText(/Failed to upload the file./)).toBeInTheDocument();
  });
});
