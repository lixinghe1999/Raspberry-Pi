package com.gtappdevelopers.camviewlibrary;

import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;

import android.content.pm.PackageManager;
import android.media.MediaPlayer;
import android.media.MediaRecorder;
import android.os.Bundle;


import android.os.Environment;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import java.io.IOException;
import java.io.InputStream;
import java.nio.file.Paths;
import java.nio.file.Files;
import java.io.File;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Date;
import java.text.SimpleDateFormat;
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
                try {
                    startRecording();
                } catch (IOException e) {
                    throw new RuntimeException(e);
                }
            }
        });
        stopTV.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                //pause Recording method will pause the recording of audio.
                pauseRecording();

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

            mFileName = foldername + "/" + timestring() + ".3gp";
            Log.d("fname", mFileName);
            //below method is used to initialize the media recorder clss
            mRecorder = new MediaRecorder();
            //below method is used to set the audio source which we are using a mic.
            mRecorder.setAudioSource(MediaRecorder.AudioSource.MIC);
            //below method is used to set the output format of the audio.
            mRecorder.setOutputFormat(MediaRecorder.OutputFormat.THREE_GPP);
            //below method is used to set the audio encoder for our recorded audio.
            mRecorder.setAudioEncoder(MediaRecorder.AudioEncoder.DEFAULT);
            //below method is used to set the output file location for our recorded audio
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

}