package com.ghlabspanamagmail.xivelyandroidtesis;

import android.app.ProgressDialog;
import android.os.AsyncTask;
import android.os.Handler;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.widget.TextView;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

public class Economos extends AppCompatActivity {

    private ProgressDialog pDialog;

    // URL to get contacts JSON
    private static String url = "XXXX";
    private static String API_KEY = "XXXX";

    //JSON nodos o etiquetas
    //Generales del Dispositivo
    private static final String TAG_DEVICE = "id";
    private static final String TAG_STATUS="status";
    private static final String TAG_UPDATED="updated";
    //Generales de cada DataStream
    private static final String TAG_ID="id";
    private static final String TAG_CURRENT_VALUE="current_value";
    private static final String TAG_TAGS="tags";

    //JSONArray del dispositivo
    JSONArray device = null;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_economos);

        //Llamada a async task para hacer el get con jason
        //Log.d("Respuesta","****Iniciando AsynTask****");

        new GetContacts().execute();
    }

    /**
     * Async task class to get json by making HTTP call
     * */
    private class GetContacts extends AsyncTask<Void, Void, Void> {

        @Override
        protected void onPreExecute() {
            super.onPreExecute();
            // Showing progress dialog
            pDialog = new ProgressDialog(Economos.this);
            pDialog.setMessage("Por Favor Espere");
            pDialog.setCancelable(false);
            pDialog.show();

        }

        @Override
        protected Void doInBackground(Void... arg0) {
            // Creating service handler class instance
            HTTPHandle sh = new HTTPHandle();

            // Making a request to url and getting response
            //String jsonStr = sh.makeServiceCall(url, HTTPHandle.GET);

            String jsonStr = sh.getDataStreamHTTP(url,API_KEY);

            Log.d("Respuesta: ", "> " + jsonStr);

            if (jsonStr != null) {
                try {
                    JSONObject jsonObj = new JSONObject(jsonStr);

                    // Getting JSON Array node
                    device = jsonObj.getJSONArray(TAG_DEVICE);

                    JSONObject c = device.getJSONObject(0);

                    //id = c.getString(TAG_ID);

                    //Log.i("***************",id);

                } catch (JSONException e) {
                    e.printStackTrace();
                }
            } else {
                Log.e("ServiceHandler", "Couldn't get any data from the url");
            }

            return null;
        }

        @Override
        protected void onPostExecute(Void result) {
            super.onPostExecute(result);
            // Dismiss the progress dialog
            if (pDialog.isShowing())
                pDialog.dismiss();

            //Actualiza datos

            /*Repite cada minuto*/
            new Handler().postDelayed(new Runnable() {
                @Override
                public void run() {
                    new GetContacts().execute();
                }
            }, 60*1000);

        }

    }
}
