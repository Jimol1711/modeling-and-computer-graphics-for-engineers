using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CircularMovementScript : MonoBehaviour
{
    public float speed = 2f; // Speed of rotation
    public float radius = 5f; // Radius of circular path
    private Vector3 centerPosition;
    private RaycastHit hit;

    private void Start()
    {
        centerPosition = transform.parent.position; // Get the center position from the parent (PathCenter) GameObject
    }

    private void Update()
    {
        // Calculate the position on the circle using time and the desired radius
        float angle = Time.time * speed;
        Vector3 offset = new Vector3(Mathf.Cos(angle), 0f, Mathf.Sin(angle)) * radius;

        // Set the position of the chicken model by adding the offset to the center position
        transform.position = centerPosition + offset;
        float desiredYPosition = 0.2f;
        // Perform a raycast downwards to find the terrain
        if (Physics.Raycast(transform.position + Vector3.up, Vector3.down, out hit, Mathf.Infinity))
        {
            // Set the y-coordinate of the chicken's position to the hit point on the terrain
            transform.position = new Vector3(transform.position.x, desiredYPosition, transform.position.z);
        }

        // Rotate the chicken model to face the direction of movement
        Quaternion targetRotation = Quaternion.LookRotation(centerPosition - (centerPosition + offset), Vector3.up);
        transform.rotation = Quaternion.Euler(0f, targetRotation.eulerAngles.y -90f , 0f);
    } 
}
