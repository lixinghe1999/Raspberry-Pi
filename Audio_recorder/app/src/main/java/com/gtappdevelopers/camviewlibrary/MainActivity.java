package com.gtappdevelopers.camviewlibrary;
import com.gtappdevelopers.camviewlibrary.SoundDeviceLister;

import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;

import android.content.pm.PackageManager;
import android.media.AudioDeviceInfo;
import android.media.AudioManager;
import android.media.MediaPlayer;
import android.media.MediaRecorder;
import android.media.AudioFormat;
import android.media.AudioRecord;
import android.os.Build;
import android.os.Bundle;


import android.os.Environment;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.nio.ByteBuffer;
import java.nio.ByteOrder;
import java.nio.file.Paths;
import java.nio.file.Files;
import java.io.File;
import java.util.ArrayList;
import java.util.Date;
import java.text.SimpleDateFormat;
import java.util.List;
import java.util.Random;


import static android.Manifest.permission.RECORD_AUDIO;
import static android.Manifest.permission.WRITE_EXTERNAL_STORAGE;

public class MainActivity extends AppCompatActivity {

    //Intializing all variables..
    private TextView startTV, stopTV, playTV, stopplayTV, statusTV, deleteTV, contentTV;
    private Button button1, button2, button3, button4, current_button;
    //creating a variable for medi recorder object class.
    private MediaRecorder mRecorder;
    // creating a variable for mediaplayer class
    private MediaPlayer mPlayer;
    //string variable is created for storing a file name
    private String mFileName;
    // constant for storing audio permission
    public static final int REQUEST_AUDIO_PERMISSION_CODE = 1;
    private String data_type = "clean";
    private String[] full_dataset;
    private ArrayList<String> dataset = new ArrayList<>();
    private static final int RECORDER_SAMPLERATE = 48000;
    private static final int RECORDER_CHANNELS = AudioFormat.CHANNEL_IN_STEREO;
    private static final int RECORDER_AUDIO_ENCODING = AudioFormat.ENCODING_PCM_FLOAT;
    private AudioRecord recorder = null;
    private Thread recordingThread = null;
    private boolean isRecording = false;
    public String[] LoadData(String inFile) {
        String tContents = "";
        try {
            InputStream stream = getAssets().open(inFile);
            int size = stream.available();
            Log.d("dataset size", ""+size);
            byte[] buffer = new byte[size];
            stream.read(buffer);
            stream.close();
            tContents = new String(buffer);
        } catch (IOException e) {
            // Handle exceptions here
        }
        Log.d("real data", tContents.substring(0, 50));
        String[] arrOfStr = tContents.split("\n", 0);
//        for (String a : arrOfStr)
//            Log.d("real data", a);
        return arrOfStr;
    }
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        try {
            List<String> soundDevices = SoundDeviceLister.listSoundDevices(getApplicationContext());
        } catch (IOException e) {
            throw new RuntimeException(e);
        }

        //initialize all variables with their layout items.
        statusTV = findViewById(R.id.idTVstatus);
        contentTV = findViewById(R.id.content);
        startTV = findViewById(R.id.btnRecord);
        stopTV = findViewById(R.id.btnStop);
        playTV = findViewById(R.id.btnPlay);
        stopplayTV = findViewById(R.id.btnStopPlay);
        deleteTV = findViewById(R.id.btnDelete);
        full_dataset = LoadData("aishell_transcript_v0.8.txt");

        stopTV.setBackgroundColor(getResources().getColor(R.color.gray));
        playTV.setBackgroundColor(getResources().getColor(R.color.gray));
        stopplayTV.setBackgroundColor(getResources().getColor(R.color.gray));

        deleteTV.setOnClickListener(new View.OnClickListener() {
            @Override public void onClick(View v) {
                File myFile = new File(mFileName);
                if(myFile.exists())
                    myFile.delete();
            }});
        button1 = findViewById(R.id.button1);
        button2 = findViewById(R.id.button2);
        button3 = findViewById(R.id.button3);
        button4 = findViewById(R.id.button4);
        current_button = button1;
        button1.setOnClickListener(new View.OnClickListener() {
            @Override public void onClick(View v) {data_type = "clean";
                current_button.setBackgroundColor(getResources().getColor(R.color.purple_200));
                button1.setBackgroundColor(getResources().getColor(R.color.gray));
                current_button = button1;
            }});
        button2.setOnClickListener(new View.OnClickListener() {
            @Override public void onClick(View v) {data_type = "noisy";
                current_button.setBackgroundColor(getResources().getColor(R.color.purple_200));
                button2.setBackgroundColor(getResources().getColor(R.color.gray));
                current_button = button2;}});
        button3.setOnClickListener(new View.OnClickListener() {
            @Override public void onClick(View v) {data_type = "low";
                current_button.setBackgroundColor(getResources().getColor(R.color.purple_200));
                button3.setBackgroundColor(getResources().getColor(R.color.gray));
                current_button = button3;}});
        button4.setOnClickListener(new View.OnClickListener() {
            @Override public void onClick(View v) {data_type = "silent";
                current_button.setBackgroundColor(getResources().getColor(R.color.purple_200));
                button4.setBackgroundColor(getResources().getColor(R.color.gray));
                current_button = button4;}});
        startTV.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                // start recording method will start the recording of audio.
                //startRecording();
                startRecording_New();
            }
        });
        stopTV.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                //pause Recording method will pause the recording of audio.
                // pauseRecording();
                stopRecording_New();

            }
        });
        playTV.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                // play audio method will play the audio which we have recorded
                playAudio();
            }
        });
        stopplayTV.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                // pause play method will pause the play of audio
                pausePlaying();
            }
        });
    }
    private String timestring(){
        Date todaysdate = new Date();
        SimpleDateFormat format = new SimpleDateFormat("hhmmss");
        String date = format.format(todaysdate);
        return date;
    }
    int BufferElements2Rec = 1024; // want to play 2048 (2K) since 2 bytes we use only 1024
    int BytesPerElement = 6; // 2 bytes in 16bit format
    public void startRecording_New() {
        stopTV.setBackgroundColor(getResources().getColor(R.color.purple_200));
        startTV.setBackgroundColor(getResources().getColor(R.color.gray));
        playTV.setBackgroundColor(getResources().getColor(R.color.gray));
        stopplayTV.setBackgroundColor(getResources().getColor(R.color.gray));
        recorder = new AudioRecord(
                MediaRecorder.AudioSource.MIC,
                RECORDER_SAMPLERATE, RECORDER_CHANNELS,
                RECORDER_AUDIO_ENCODING, BufferElements2Rec * BytesPerElement);

        recorder.startRecording();
        isRecording = true;
        recordingThread = new Thread(new Runnable() {
            public void run() {
                writeAudioDataToFile();
            }
        }, "AudioRecorder Thread");
        recordingThread.start();
    }
    private void writeAudioDataToFile() {
        // Write the output audio in byte

        String filePath = "/sdcard/voice8K16bitmono.pcm";
        short sData[] = new short[BufferElements2Rec];

        FileOutputStream os = null;
        try {
            os = new FileOutputStream(filePath);
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        }

        while (isRecording) {
            // gets the voice output from microphone to byte format

            recorder.read(sData, 0, BufferElements2Rec);
            System.out.println("Short writing to file" + sData.toString());
            try {
                // // writes the data to file from buffer
                // // stores the voice buffer
                byte bData[] = short2byte(sData);
                os.write(bData, 0, BufferElements2Rec * BytesPerElement);
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
        try {
            os.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
    public void stopRecording_New() {
        stopTV.setBackgroundColor(getResources().getColor(R.color.gray));
        startTV.setBackgroundColor(getResources().getColor(R.color.purple_200));
        playTV.setBackgroundColor(getResources().getColor(R.color.purple_200));
        stopplayTV.setBackgroundColor(getResources().getColor(R.color.purple_200));
        if (null != recorder) {
            isRecording = false;
            recorder.stop();
            recorder.release();
            recorder = null;
            recordingThread = null;
        }
//        File f1 = new File("/sdcard/voice8K16bitmono.pcm"); // The location of your PCM file
//        File f2 = new File("/sdcard/voice8K16bitmono.wav"); // The location where you want your WAV file
//        try {
//            rawToWave(f1, f2);
//        } catch (IOException e) {
//            e.printStackTrace();
//        }
    }
    private byte[] short2byte(short[] sData) {
        int shortArrsize = sData.length;
        byte[] bytes = new byte[shortArrsize * 2];
        for (int i = 0; i < shortArrsize; i++) {
            bytes[i * 2] = (byte) (sData[i] & 0x00FF);
            bytes[(i * 2) + 1] = (byte) (sData[i] >> 8);
            sData[i] = 0;
        }
        return bytes;

    }

    private void startRecording() throws IOException {
        Log.d("data type", data_type);
        // check permission method is used to check that the user has granted permission to record nd store the audio.
        if (CheckPermissions()) {
            Random random = new Random();
            int random_index = random.nextInt(full_dataset.length);
            String sentence = full_dataset[random_index];
            sentence = sentence.substring(17);
            Log.d("sentence", sentence);
            contentTV.setText(sentence);
            dataset.add(sentence);

            //setbackgroundcolor method will change the background color of text view.
            stopTV.setBackgroundColor(getResources().getColor(R.color.purple_200));
            startTV.setBackgroundColor(getResources().getColor(R.color.gray));
            playTV.setBackgroundColor(getResources().getColor(R.color.gray));
            stopplayTV.setBackgroundColor(getResources().getColor(R.color.gray));
            //we are here initializing our filename variable with the path of the recorded audio file.
            String foldername = Environment.getExternalStorageDirectory().getAbsolutePath() + "/VibVoice";
            EditText name = findViewById(R.id.name);
            foldername +=  "/" + data_type + "/" + name.getText().toString() ;
            Files.createDirectories(Paths.get(foldername));

            mFileName = foldername + "/" + timestring() + ".wav";
            Log.d("fname", mFileName);
            //below method is used to initialize the media recorder clss
            mRecorder = new MediaRecorder();
            //below method is used to set the audio source which we are using a mic.
            mRecorder.setAudioSource(MediaRecorder.AudioSource.CAMCORDER);
            //below method is used to set the output format of the audio.
            mRecorder.setOutputFormat(MediaRecorder.OutputFormat.DEFAULT);
            //below method is used to set the audio encoder for our recorded audio.
            mRecorder.setAudioEncoder(MediaRecorder.AudioEncoder.DEFAULT);
            //below method is used to set the output file location for our recorded audio
            mRecorder.setAudioChannels(2);
            mRecorder.setAudioSamplingRate(16000);
            mRecorder.setOutputFile(mFileName);
            try {
                //below mwthod will prepare our audio recorder class
                mRecorder.prepare();
            } catch (IOException e) {
                Log.e("TAG", "prepare() failed");
            }
            // start method will start the audio recording.
            mRecorder.start();
            statusTV.setText("Recording Started");
        } else {
            //if audio recording permissions are not granted by user below method will ask for runtime permission for mic and storage.
            RequestPermissions();
        }
    }

    @Override
    public void onRequestPermissionsResult(int requestCode, String[] permissions, int[] grantResults) {
        // this method is called when user will grant the permission for audio recording.
        switch (requestCode) {
            case REQUEST_AUDIO_PERMISSION_CODE:
                if (grantResults.length > 0) {
                    boolean permissionToRecord = grantResults[0] == PackageManager.PERMISSION_GRANTED;
                    boolean permissionToStore = grantResults[1] == PackageManager.PERMISSION_GRANTED;
                    if (permissionToRecord && permissionToStore) {
                        Toast.makeText(getApplicationContext(), "Permission Granted", Toast.LENGTH_LONG).show();
                    } else {
                        Toast.makeText(getApplicationContext(), "Permission Denied", Toast.LENGTH_LONG).show();
                    }
                }
                break;
        }
    }

    public boolean CheckPermissions() {
        //this method is used to check permission
        int result = ContextCompat.checkSelfPermission(getApplicationContext(), WRITE_EXTERNAL_STORAGE);
        int result1 = ContextCompat.checkSelfPermission(getApplicationContext(), RECORD_AUDIO);
        return result == PackageManager.PERMISSION_GRANTED && result1 == PackageManager.PERMISSION_GRANTED;
    }

    private void RequestPermissions() {
        // this method is used to request the permission for audio recording and storage.
        ActivityCompat.requestPermissions(MainActivity.this, new String[]{RECORD_AUDIO, WRITE_EXTERNAL_STORAGE}, REQUEST_AUDIO_PERMISSION_CODE);
    }


    public void playAudio() {
        stopTV.setBackgroundColor(getResources().getColor(R.color.gray));
        startTV.setBackgroundColor(getResources().getColor(R.color.purple_200));
        playTV.setBackgroundColor(getResources().getColor(R.color.gray));
        stopplayTV.setBackgroundColor(getResources().getColor(R.color.purple_200));
        //for playing our recorded audio we are using media player class.
        mPlayer = new MediaPlayer();
        try {
            //below method is used to set the data source which will be our file name
            mPlayer.setDataSource(mFileName);
            //below method will prepare our media player
            mPlayer.prepare();
            //below method will start our media player.
            mPlayer.start();
            statusTV.setText("Recording Started Playing");
        } catch (IOException e) {
            Log.e("TAG", "prepare() failed");
        }


    }

    public void pauseRecording() {
        stopTV.setBackgroundColor(getResources().getColor(R.color.gray));
        startTV.setBackgroundColor(getResources().getColor(R.color.purple_200));
        playTV.setBackgroundColor(getResources().getColor(R.color.purple_200));
        stopplayTV.setBackgroundColor(getResources().getColor(R.color.purple_200));
        //below method will stop the audio recording.
        mRecorder.stop();
        //below method will release the media recorder class.
        mRecorder.release();
        mRecorder = null;
        statusTV.setText("Recording Stopped");

    }

    public void pausePlaying() {
        //this method will release the media player class and pause the playing of our recorded audio.
        mPlayer.release();
        mPlayer = null;
        stopTV.setBackgroundColor(getResources().getColor(R.color.gray));
        startTV.setBackgroundColor(getResources().getColor(R.color.purple_200));
        playTV.setBackgroundColor(getResources().getColor(R.color.purple_200));
        stopplayTV.setBackgroundColor(getResources().getColor(R.color.gray));
        statusTV.setText("Recording Play Stopped");

    }
    private void rawToWave(final File rawFile, final File waveFile) throws IOException {

        byte[] rawData = new byte[(int) rawFile.length()];
        DataInputStream input;
        input = null;
        try {
            input = new DataInputStream(new FileInputStream(rawFile));
            input.read(rawData);
        } finally {
            if (input != null) {
                input.close();
            }
        }

        DataOutputStream output = null;
        try {
            output = new DataOutputStream(new FileOutputStream(waveFile));
            // WAVE header
            // see http://ccrma.stanford.edu/courses/422/projects/WaveFormat/
            writeString(output, "RIFF"); // chunk id
            writeInt(output, 36 + rawData.length); // chunk size
            writeString(output, "WAVE"); // format
            writeString(output, "fmt "); // subchunk 1 id
            writeInt(output, 16); // subchunk 1 size
            writeShort(output, (short) 1); // audio format (1 = PCM)
            writeShort(output, (short) 2); // number of channels
            writeInt(output, 44100); // sample rate
            writeInt(output, RECORDER_SAMPLERATE * 2); // byte rate
            writeShort(output, (short) 2); // block align
            writeShort(output, (short) 16); // bits per sample
            writeString(output, "data"); // subchunk 2 id
            writeInt(output, rawData.length); // subchunk 2 size
            // Audio data (conversion big endian -> little endian)
            short[] shorts = new short[rawData.length / 2];
            ByteBuffer.wrap(rawData).order(ByteOrder.LITTLE_ENDIAN).asShortBuffer().get(shorts);
            ByteBuffer bytes = ByteBuffer.allocate(shorts.length * 2);
            for (short s : shorts) {
                bytes.putShort(s);
            }

            output.write(fullyReadFileToBytes(rawFile));
        } finally {
            if (output != null) {
                output.close();
            }
        }
    }
    byte[] fullyReadFileToBytes(File f) throws IOException {
        int size = (int) f.length();
        byte bytes[] = new byte[size];
        byte tmpBuff[] = new byte[size];
        FileInputStream fis= new FileInputStream(f);
        try {

            int read = fis.read(bytes, 0, size);
            if (read < size) {
                int remain = size - read;
                while (remain > 0) {
                    read = fis.read(tmpBuff, 0, remain);
                    System.arraycopy(tmpBuff, 0, bytes, size - remain, read);
                    remain -= read;
                }
            }
        }  catch (IOException e){
            throw e;
        } finally {
            fis.close();
        }

        return bytes;
    }
    private void writeInt(final DataOutputStream output, final int value) throws IOException {
        output.write(value >> 0);
        output.write(value >> 8);
        output.write(value >> 16);
        output.write(value >> 24);
    }

    private void writeShort(final DataOutputStream output, final short value) throws IOException {
        output.write(value >> 0);
        output.write(value >> 8);
    }

    private void writeString(final DataOutputStream output, final String value) throws IOException {
        for (int i = 0; i < value.length(); i++) {
            output.write(value.charAt(i));
        }
    }
}