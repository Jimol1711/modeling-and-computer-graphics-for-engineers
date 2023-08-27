using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class WindmillRotation : MonoBehaviour
{
    public float rotationSpeed;
    public GameObject pivotObject;

    private Vector3 initialPosition;
    public float xRotation = 0f;
    public float yRotation = 0f;
    public float zRotation = 0f;


    // Start is called before the first frame update
    
    void Start()
    {
        // Store the initial position
        initialPosition = transform.position;

    }

    // Update is called once per frame

    void Update()
    {
        transform.RotateAround(pivotObject.transform.position, new Vector3(1, 0, 0), rotationSpeed * Time.deltaTime);
        transform.position = initialPosition; // Maintain the fixed position
        // xRotation += 2f;
        // Quaternion currentRotation = transform.localRotation;
        // Quaternion newRotation = Quaternion.Euler(xRotation, yRotation, zRotation);
        // transform.localRotation = newRotation;
    }
}


