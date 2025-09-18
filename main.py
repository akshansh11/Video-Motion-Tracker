# -*- coding: utf-8 -*-
"""
Created on Thu Sep 18 21:25:40 2025

@author: Akshansh Mishra
"""

import cv2
import numpy as np
from collections import deque
import random

class PersonSilhouetteTracker:
    def __init__(self, trail_length=15, contour_thickness=3):
        self.trail_length = trail_length
        self.contour_thickness = contour_thickness
        self.bg_subtractor = cv2.createBackgroundSubtractorMOG2(detectShadows=False)
        
        # Store multiple frames of contours with colors
        self.contour_history = deque(maxlen=trail_length)
        
        # Rainbow colors for the trail effect
        self.colors = [
            (255, 0, 0),    # Red
            (255, 127, 0),  # Orange
            (255, 255, 0),  # Yellow
            (127, 255, 0),  # Light Green
            (0, 255, 0),    # Green
            (0, 255, 127),  # Teal
            (0, 255, 255),  # Cyan
            (0, 127, 255),  # Light Blue
            (0, 0, 255),    # Blue
            (127, 0, 255),  # Purple
            (255, 0, 255),  # Magenta
            (255, 0, 127),  # Pink
        ]
        
    def process_video(self, video_path, output_path=None):
        cap = cv2.VideoCapture(video_path)
        
        if output_path:
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            fps = int(cap.get(cv2.CAP_PROP_FPS))
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        
        frame_count = 0
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Get motion mask
            fg_mask = self.bg_subtractor.apply(frame)
            
            # Clean up the mask
            kernel = np.ones((5, 5), np.uint8)
            fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_CLOSE, kernel)
            fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_OPEN, kernel)
            
            # Find contours of the person
            contours, _ = cv2.findContours(fg_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            # Filter for significant contours (person-sized)
            person_contours = []
            for contour in contours:
                area = cv2.contourArea(contour)
                if area > 1000:  # Adjust this value based on your video
                    person_contours.append(contour)
            
            # Add current contours to history
            if person_contours:
                self.contour_history.append(person_contours)
            
            # Create the result frame with trails
            result_frame = self.draw_silhouette_trails(frame.copy())
            
            # Display frame
            cv2.imshow('Person Silhouette Tracker', result_frame)
            
            if output_path:
                out.write(result_frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
            frame_count += 1
        
        cap.release()
        if output_path:
            out.release()
        cv2.destroyAllWindows()
    
    def draw_silhouette_trails(self, frame):
        # Draw trails from oldest to newest
        for i, contours in enumerate(self.contour_history):
            # Calculate alpha (transparency) - newer frames are more opaque
            alpha = (i + 1) / len(self.contour_history)
            
            # Get color for this trail layer
            color_idx = i % len(self.colors)
            color = self.colors[color_idx]
            
            # Create overlay for this trail layer
            overlay = frame.copy()
            
            # Draw all contours for this frame
            for contour in contours:
                # Draw filled silhouette with some transparency
                cv2.fillPoly(overlay, [contour], color)
                
                # Draw contour outline
                cv2.drawContours(overlay, [contour], -1, color, self.contour_thickness)
            
            # Blend with original frame using alpha
            cv2.addWeighted(overlay, alpha * 0.3, frame, 1 - alpha * 0.3, 0, frame)
        
        return frame

class EdgeTrailTracker:
    def __init__(self, trail_length=20):
        self.trail_length = trail_length
        self.bg_subtractor = cv2.createBackgroundSubtractorMOG2(detectShadows=False)
        self.edge_history = deque(maxlen=trail_length)
        
        # More vibrant colors
        self.colors = [
            (0, 255, 255),   # Cyan
            (255, 0, 255),   # Magenta  
            (255, 255, 0),   # Yellow
            (0, 255, 0),     # Green
            (255, 0, 0),     # Red
            (0, 0, 255),     # Blue
            (255, 127, 0),   # Orange
            (127, 0, 255),   # Purple
        ]
        
    def process_video(self, video_path, output_path=None):
        cap = cv2.VideoCapture(video_path)
        
        if output_path:
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            fps = int(cap.get(cv2.CAP_PROP_FPS))
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Get motion mask
            fg_mask = self.bg_subtractor.apply(frame)
            
            # Clean up mask
            kernel = np.ones((3, 3), np.uint8)
            fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_CLOSE, kernel)
            fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_OPEN, kernel)
            
            # Get edges of moving objects
            edges = cv2.Canny(fg_mask, 50, 150)
            
            # Add current edges to history
            self.edge_history.append(edges.copy())
            
            # Create result with colorful edge trails
            result_frame = self.draw_edge_trails(frame.copy())
            
            cv2.imshow('Edge Trail Tracker', result_frame)
            
            if output_path:
                out.write(result_frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cap.release()
        if output_path:
            out.release()
        cv2.destroyAllWindows()
    
    def draw_edge_trails(self, frame):
        # Create colored trails from edge history
        for i, edges in enumerate(self.edge_history):
            alpha = (i + 1) / len(self.edge_history)
            color_idx = i % len(self.colors)
            color = self.colors[color_idx]
            
            # Find edge pixels
            edge_points = np.where(edges > 0)
            
            if len(edge_points[0]) > 0:
                # Create colored overlay for edges
                overlay = frame.copy()
                overlay[edge_points] = color
                
                # Blend with main frame
                cv2.addWeighted(overlay, alpha * 0.6, frame, 1 - alpha * 0.6, 0, frame)
        
        return frame

class ParticleTrailTracker:
    def __init__(self, trail_length=30, num_particles=200):
        self.trail_length = trail_length
        self.num_particles = num_particles
        self.bg_subtractor = cv2.createBackgroundSubtractorMOG2(detectShadows=False)
        self.particles = []
        
        # Particle colors
        self.colors = [
            (255, 100, 100), (100, 255, 100), (100, 100, 255),
            (255, 255, 100), (255, 100, 255), (100, 255, 255),
            (255, 150, 0), (150, 0, 255), (0, 255, 150)
        ]
        
    def process_video(self, video_path, output_path=None):
        cap = cv2.VideoCapture(video_path)
        
        if output_path:
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            fps = int(cap.get(cv2.CAP_PROP_FPS))
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Get motion mask
            fg_mask = self.bg_subtractor.apply(frame)
            
            # Clean mask
            kernel = np.ones((5, 5), np.uint8)
            fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_CLOSE, kernel)
            
            # Update particles based on motion
            self.update_particles(fg_mask)
            
            # Draw particle trails
            result_frame = self.draw_particle_trails(frame.copy())
            
            cv2.imshow('Particle Trail Tracker', result_frame)
            
            if output_path:
                out.write(result_frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cap.release()
        if output_path:
            out.release()
        cv2.destroyAllWindows()
    
    def update_particles(self, mask):
        # Find motion areas
        motion_points = np.where(mask > 0)
        
        if len(motion_points[0]) > 0:
            # Sample random points from motion areas
            indices = np.random.choice(len(motion_points[0]), 
                                     min(self.num_particles, len(motion_points[0])), 
                                     replace=False)
            
            for idx in indices:
                y, x = motion_points[0][idx], motion_points[1][idx]
                color = random.choice(self.colors)
                
                particle = {
                    'trail': deque([(x, y)], maxlen=self.trail_length),
                    'color': color,
                    'life': self.trail_length
                }
                self.particles.append(particle)
        
        # Update existing particles
        active_particles = []
        for particle in self.particles:
            particle['life'] -= 1
            if particle['life'] > 0:
                active_particles.append(particle)
        
        self.particles = active_particles
    
    def draw_particle_trails(self, frame):
        for particle in self.particles:
            trail = list(particle['trail'])
            color = particle['color']
            
            # Draw trail
            for i in range(1, len(trail)):
                alpha = i / len(trail)
                thickness = max(1, int(3 * alpha))
                cv2.line(frame, trail[i-1], trail[i], color, thickness)
            
            # Draw particle
            if trail:
                cv2.circle(frame, trail[-1], 2, color, -1)
        
        return frame

# Usage example
if __name__ == "__main__":
    print("Choose tracking method:")
    print("1. Silhouette Trails (colorful silhouette outlines)")
    print("2. Edge Trails (colorful edge detection)")  
    print("3. Particle Trails (particle system following motion)")
    
    choice = input("Enter choice (1, 2, or 3): ")
    
    video_path = "C:/Users/pedit/Downloads/deadpool.mp4"  # Replace with your video path
    output_path = "C:/Users/pedit/Downloads/tracked_output2.mp4"
    
    if choice == "1":
        tracker = PersonSilhouetteTracker(trail_length=15, contour_thickness=3)
    elif choice == "2":
        tracker = EdgeTrailTracker(trail_length=20)
    else:
        tracker = ParticleTrailTracker(trail_length=30, num_particles=10000)
    
    tracker.process_video(video_path, output_path)
