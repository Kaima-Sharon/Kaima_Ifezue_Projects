#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <math.h>
#include "phylib.h"

//PART 1

//creates a new still ball
phylib_object *phylib_new_still_ball( unsigned char number, phylib_coord *pos ){
    phylib_object *billardObj = (phylib_object*) malloc(sizeof(phylib_object));

    if(billardObj == NULL){
        return NULL;
    }

    billardObj->type = PHYLIB_STILL_BALL;
    
    phylib_still_ball* newStillBall = (phylib_still_ball*) malloc(sizeof(phylib_still_ball));

    if(newStillBall == NULL){
        return NULL;
    }
    newStillBall->number = number;
    newStillBall->pos = *pos;

    billardObj->obj.still_ball = *newStillBall;

    return billardObj;
}

//creates a new rolling ball
phylib_object *phylib_new_rolling_ball( unsigned char number, phylib_coord *pos, phylib_coord *vel, phylib_coord *acc ){
    phylib_object *billardObj = (phylib_object*) malloc(sizeof(phylib_object));

    if(billardObj == NULL){
        return NULL;
    }

    billardObj->type = PHYLIB_ROLLING_BALL;

    phylib_rolling_ball* newRollingBall = (phylib_rolling_ball*)malloc(sizeof(phylib_rolling_ball));
    newRollingBall->number = number;
    newRollingBall->pos = *pos;
    newRollingBall->vel = *vel;
    newRollingBall->acc = *acc;

    billardObj->obj.rolling_ball = *newRollingBall;

    return billardObj;
}

//creates a new hole
phylib_object *phylib_new_hole( phylib_coord *pos ){
    phylib_object *billardObj = (phylib_object*)malloc(sizeof(phylib_object));

    if(billardObj == NULL){
        return NULL;
    }

    billardObj->type = PHYLIB_HOLE;

    billardObj->obj.hole.pos = *pos;

    return billardObj;
}

//creates a new horizontal cushion
phylib_object *phylib_new_hcushion( double y ){
    phylib_object* billardObj = (phylib_object*)malloc(sizeof(phylib_object));
    
    if(billardObj == NULL){
        return NULL;
    }

    billardObj->type = PHYLIB_HCUSHION;

    billardObj->obj.hcushion.y = y;

    return billardObj;
}

//creates a new vertical cushion
phylib_object *phylib_new_vcushion( double x ){

    phylib_object* billardObj = (phylib_object*)malloc(sizeof(phylib_object));
    
    if(billardObj == NULL){
        return NULL;
    }

    billardObj->type = PHYLIB_VCUSHION;

    billardObj->obj.vcushion.x = x;

    return billardObj;
}

//creates new coordinates
phylib_coord *coordinates(double x, double y){
    phylib_coord *setCoordinates = (phylib_coord *)malloc(sizeof(phylib_coord));

    setCoordinates->x = x;
    setCoordinates->y = y;

    return setCoordinates;
}

//creates a new table
phylib_table *phylib_new_table(void){
    phylib_table* billardTable = (phylib_table*)malloc(sizeof(phylib_table));

    if(billardTable == NULL){
        return NULL;
    }

    billardTable->time = 0.0;

    billardTable->object[0] = phylib_new_hcushion(0);
    billardTable->object[1] = phylib_new_hcushion(PHYLIB_TABLE_LENGTH);
    billardTable->object[2] = phylib_new_vcushion(0);
    billardTable->object[3] = phylib_new_vcushion(PHYLIB_TABLE_WIDTH);
    billardTable->object[4] = phylib_new_hole(coordinates(0, 0));
    billardTable->object[5] = phylib_new_hole(coordinates(PHYLIB_TABLE_WIDTH, 0));
    billardTable->object[6] = phylib_new_hole(coordinates(0, PHYLIB_TABLE_LENGTH));
    billardTable->object[7] = phylib_new_hole(coordinates(PHYLIB_TABLE_WIDTH, PHYLIB_TABLE_WIDTH));
    billardTable->object[8] = phylib_new_hole(coordinates(0, PHYLIB_TABLE_WIDTH));
    billardTable->object[9] = phylib_new_hole(coordinates(PHYLIB_TABLE_WIDTH, PHYLIB_TABLE_LENGTH));

    for(int i = 10; i < PHYLIB_MAX_OBJECTS; i++){
        billardTable->object[i] = NULL;
    }

    return billardTable;
}

// PART 2

//copies an object 
void phylib_copy_object( phylib_object **dest, phylib_object **src ){
    phylib_object* newBillardObj = (phylib_object*)malloc(sizeof(phylib_object));

    //check if src is NULL
    if(*src == NULL){
        *dest = NULL;
        return;
    }

    memcpy(newBillardObj, *src, sizeof(phylib_object));

    *dest = (phylib_object*)malloc(sizeof(phylib_object));
    
    *dest = newBillardObj;
}

//copies a table
phylib_table *phylib_copy_table( phylib_table *table){
    if(table == NULL){
        return NULL;
    }

    phylib_table* newTable = (phylib_table*)malloc(sizeof(phylib_table));

    if(newTable == NULL){
        return NULL;
    }

    for(int i = 0; i < PHYLIB_MAX_OBJECTS; i++){
        phylib_copy_object(&(newTable->object[i]), &(table->object[i]));
    }

    newTable->time = table->time;
    return newTable;
}

//adds an object to table
void phylib_add_object( phylib_table *table, phylib_object *object){
    for(int i = 0; i < PHYLIB_MAX_OBJECTS; i++){
        if(table->object[i] == NULL){
            table->object[i] = object;
            return;
        }
    }
}

//frees table
void phylib_free_table( phylib_table *table ){
    int i = 0;

    for(i = 0; i < PHYLIB_MAX_OBJECTS; i++){
        if(table->object[i] != NULL){
            free(table->object[i]);
            table->object[i] = NULL;
        }
    }

    free(table);
}

//subtracts one coordinate from another
phylib_coord phylib_sub( phylib_coord c1, phylib_coord c2 ){
    double xSubResult;
    double ySubResult;

    xSubResult = c1.x - c2.x;
    ySubResult = c1.y - c2.y;

    phylib_coord newCoord;

    newCoord.x = xSubResult;
    newCoord.y = ySubResult;

    return newCoord;
}

//gets the length of a coordinate
double phylib_length( phylib_coord c ){
    double coordLength = 0.0;
    double coordLengthSqr = 0.0;

    //pythagoras theorem
    coordLengthSqr = ((c.x)*(c.x)) + ((c.y)*(c.y));

    coordLength = sqrt(coordLengthSqr);

    return coordLength;
}

//gets the dot product of two coordinates
double phylib_dot_product( phylib_coord a, phylib_coord b ){
    double dotProd;

    dotProd = ((a.x)*(b.x)) + ((a.y)*(b.y));

    return dotProd;
}

//helper function for phylib_distance
double distanceFunc(double xDiff, double yDiff){
    double distance = 0;
    double xSqr = xDiff * xDiff;
    double ySqr = yDiff * yDiff;

    distance = sqrt(xSqr + ySqr);

    return distance;
}

//calculates the distance between to objects
double phylib_distance( phylib_object *obj1, phylib_object *obj2 ){
    if(obj1 == NULL || obj2 == NULL){
        return -1.0;
    }

    double xDiff = 0.0;
    double yDiff = 0.0;
    double distance, finalDist = 0.0;

    if(obj1->type != PHYLIB_ROLLING_BALL){
        //printf("Invalid object type\n");
        return -1.0;
    }

    if(obj2->type == PHYLIB_ROLLING_BALL || obj2->type == PHYLIB_STILL_BALL){
        if(obj2->type == PHYLIB_ROLLING_BALL){
            xDiff = (obj2->obj.rolling_ball.pos.x) - (obj1->obj.rolling_ball.pos.x);
            yDiff = (obj2->obj.rolling_ball.pos.y) - (obj1->obj.rolling_ball.pos.y);
        }
        else if(obj2->type == PHYLIB_STILL_BALL){
            xDiff = (obj2->obj.still_ball.pos.x) - (obj1->obj.rolling_ball.pos.x);
            yDiff = (obj2->obj.still_ball.pos.y) - (obj1->obj.rolling_ball.pos.y);
        }
        distance = distanceFunc(xDiff, yDiff);
        finalDist = distance - PHYLIB_BALL_DIAMETER;
    }
    else if(obj2->type == PHYLIB_HOLE){
        xDiff = (obj2->obj.hole.pos.x) - (obj1->obj.rolling_ball.pos.x);
        yDiff = (obj2->obj.hole.pos.y) - (obj1->obj.rolling_ball.pos.y);

        distance = distanceFunc(xDiff, yDiff);
        finalDist = distance - PHYLIB_HOLE_RADIUS;
    }
    else if(obj2->type == PHYLIB_HCUSHION || obj2->type == PHYLIB_VCUSHION){
        if(obj2->type == PHYLIB_HCUSHION){
            //x is 0
            xDiff = fabs((obj1->obj.rolling_ball.pos.x) - 0);
            yDiff = fabs((obj1->obj.rolling_ball.pos.y) - (obj1->obj.hcushion.y));
        }
        else if(obj2->type == PHYLIB_VCUSHION){
            //y is 0
            xDiff = fabs((obj2->obj.vcushion.x) - (obj1->obj.rolling_ball.pos.x));
            yDiff = fabs((obj1->obj.rolling_ball.pos.y) - 0);
        }

        distance = distanceFunc(xDiff, yDiff);
        finalDist = distance - PHYLIB_BALL_RADIUS;
    }

    return finalDist;
}

//PART 3
void phylib_roll( phylib_object *new, phylib_object *old, double time ){
    if(new->type == PHYLIB_ROLLING_BALL & old->type == PHYLIB_ROLLING_BALL){
        phylib_coord vOne = old->obj.rolling_ball.vel;
        phylib_coord pOne = old->obj.rolling_ball.pos;
        phylib_coord aOne = old->obj.rolling_ball.acc;

        new->obj.rolling_ball.pos.x = pOne.x + ((vOne.x)*time) + (0.5*(aOne.x)*(time*time));
        new->obj.rolling_ball.pos.y = pOne.y + ((vOne.y)*time) + (0.5*(aOne.y)*(time*time));
        new->obj.rolling_ball.vel.x = vOne.x + (aOne.x) * time; 
        new->obj.rolling_ball.vel.y = vOne.y + (aOne.y) * time;

        if((vOne.x >= 0 && new->obj.rolling_ball.vel.x < 0) || (vOne.x < 0 && new->obj.rolling_ball.vel.x >= 0)){
            new->obj.rolling_ball.vel.x = 0.0;
            new->obj.rolling_ball.acc.x = 0.0;
        }
        if((vOne.y >= 0 && new->obj.rolling_ball.vel.y < 0) || (vOne.y < 0 && new->obj.rolling_ball.vel.y >= 0)){
            new->obj.rolling_ball.pos.y = 0.0;
            new->obj.rolling_ball.acc.y = 0.0;
        }
    }
}

unsigned char phylib_stopped( phylib_object *object ){

    if(object == NULL){
        return 0;
    }

    if(object->type != PHYLIB_ROLLING_BALL){
        return 0;
    }
    double velLength = phylib_length(object->obj.rolling_ball.vel);

    if(velLength < PHYLIB_VEL_EPSILON){
        object->type = PHYLIB_STILL_BALL;
        object->obj.still_ball.number = object->obj.rolling_ball.number;
        object->obj.still_ball.pos = object->obj.rolling_ball.pos;
        return 1;
    }
    else{
        return 0;
    }
}

void phylib_bounce(phylib_object **a, phylib_object **b){
    if((*a) == NULL || (*b) == NULL){
        return;
    }

    switch((*b)->type){
        case PHYLIB_HCUSHION:
            (*a)->obj.rolling_ball.vel.y = (*a)->obj.rolling_ball.vel.y * (-1.0);
            (*a)->obj.rolling_ball.acc.y = (*a)->obj.rolling_ball.acc.y * (-1.0);
            break;
        case PHYLIB_VCUSHION:
            (*a)->obj.rolling_ball.vel.x = (*a)->obj.rolling_ball.vel.x * (-1.0);
            (*a)->obj.rolling_ball.acc.x = (*a)->obj.rolling_ball.acc.x * (-1.0);
            break;
        case PHYLIB_HOLE:
            free(*a);
            (*a) = NULL;
            break;
        case PHYLIB_STILL_BALL:
            (*b)->type = PHYLIB_ROLLING_BALL;
            (*b)->obj.rolling_ball.number = (*b)->obj.still_ball.number;
            (*b)->obj.rolling_ball.pos = (*b)->obj.still_ball.pos;
            (*b)->obj.rolling_ball.vel.x = 0.0;
            (*b)->obj.rolling_ball.vel.y = 0.0;
            (*b)->obj.rolling_ball.acc.x = 0.0;
            (*b)->obj.rolling_ball.acc.y = 0.0;
        case PHYLIB_ROLLING_BALL:
            {
            //if((*a) != NULL){
                phylib_coord r_ab;
                phylib_coord v_rel;
                phylib_coord n;
                double v_rel_n;

                r_ab.x = (*a)->obj.rolling_ball.pos.x - (*b)->obj.rolling_ball.pos.x;
                r_ab.y = (*a)->obj.rolling_ball.pos.y - (*b)->obj.rolling_ball.pos.y;

                v_rel.x = (*a)->obj.rolling_ball.vel.x - (*b)->obj.rolling_ball.vel.x;
                v_rel.y = (*a)->obj.rolling_ball.vel.y - (*b)->obj.rolling_ball.vel.y;

                n.x = (r_ab.x)/phylib_length(r_ab);
                n.y = (r_ab.y)/phylib_length(r_ab);

                v_rel_n = phylib_dot_product(v_rel, n);

                (*a)->obj.rolling_ball.vel.x = (*a)->obj.rolling_ball.vel.x - (v_rel_n * (n.x));
                (*a)->obj.rolling_ball.vel.y = (*a)->obj.rolling_ball.vel.y - (v_rel_n * (n.y));

                (*b)->obj.rolling_ball.pos.x = (*b)->obj.rolling_ball.pos.x + (v_rel_n * (n.x));
                (*b)->obj.rolling_ball.pos.y = (*b)->obj.rolling_ball.pos.y + (v_rel_n * (n.y));

                double aSpeed = phylib_length((*a)->obj.rolling_ball.vel);
                double bSpeed = phylib_length((*b)->obj.rolling_ball.vel);

                if(aSpeed > PHYLIB_VEL_EPSILON){
                    (*a)->obj.rolling_ball.acc.x = (-(*a)->obj.rolling_ball.vel.x) / (aSpeed * PHYLIB_DRAG);
                    (*a)->obj.rolling_ball.acc.y = (-(*a)->obj.rolling_ball.vel.y) / (aSpeed * PHYLIB_DRAG);
                }

                if(bSpeed > PHYLIB_VEL_EPSILON){
                    (*b)->obj.rolling_ball.acc.x = (-(*b)->obj.rolling_ball.vel.x) / (bSpeed * PHYLIB_DRAG);
                    (*b)->obj.rolling_ball.acc.y = (-(*b)->obj.rolling_ball.vel.y) / (bSpeed * PHYLIB_DRAG);
                }
            //}
            }
            break;
        default:
            break;
    }
}

unsigned char phylib_rolling (phylib_table *t){
    unsigned char numRolling = 0;
    for(int i = 0; i < PHYLIB_MAX_OBJECTS; i++){
        if(t->object[i] != NULL && t->object[i]->type == PHYLIB_ROLLING_BALL){
            numRolling = numRolling + 1;
        }
    }
    return numRolling;
}

// phylib_table *phylib_segment (phylib_table *table){ 

//     if(phylib_rolling(table) == 0){
//         return NULL;
//     }

//     phylib_table *newTable = phylib_copy_table(table);

//     double time = PHYLIB_SIM_RATE;

//     while(time < PHYLIB_MAX_TIME){
//         for(int i = 0; i < PHYLIB_MAX_OBJECTS; i++){
//             if(newTable->object[i] != NULL && newTable->object[i]->type == PHYLIB_ROLLING_BALL){
//                 phylib_roll(newTable->object[i], newTable->object[i], PHYLIB_SIM_RATE);
//                 if((phylib_stopped(newTable->object[i]))){
//                     newTable->time = time;
//                     return newTable;
//                 }
//             }
//         }
//         for(int i = 0; i < PHYLIB_MAX_OBJECTS; i++){
//             if(newTable->object[i] != NULL && newTable->object[i]->type == PHYLIB_ROLLING_BALL){
//                 for(int j = 0; j < PHYLIB_MAX_OBJECTS; j++){
//                     if(newTable->object[j] != NULL){
//                         if((i != j && phylib_distance(newTable->object[i], newTable->object[j])) < 0.0){
//                             phylib_bounce(&newTable->object[i], &newTable->object[j]);
//                             newTable->time = time;
//                             return newTable;
//                         } 
//                     }
//                 }
//             } 
//         }
//         time += PHYLIB_SIM_RATE;
//     }
//     newTable->time = time;
//     return newTable;
// }

phylib_table *phylib_segment(phylib_table *table) {

    if (phylib_rolling(table) == 0) {
        return NULL;
    }

    phylib_table * newTable = phylib_copy_table(table);
    double time = table->time + PHYLIB_SIM_RATE;

    while (time < PHYLIB_MAX_TIME) {
        for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++) {
            if (newTable->object[i] && newTable->object[i]->type == PHYLIB_ROLLING_BALL) {
                phylib_roll(newTable->object[i], newTable->object[i], PHYLIB_SIM_RATE); 
                if (phylib_stopped(newTable->object[i])) {
                    newTable->time = time; 
                    return newTable;
                }
            }
        }

        for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++) {
            if (newTable->object[i] && newTable->object[i]->type == PHYLIB_ROLLING_BALL) {
                for (int j = 0; j < PHYLIB_MAX_OBJECTS; j++) {
                    if (newTable->object[j] && i != j && phylib_distance(newTable->object[i], newTable->object[j]) < 0.0) {
                        phylib_bounce(&newTable->object[i], &newTable->object[j]);
                        newTable->time = time; 
                        return newTable;
                    }
                }
            }
        }

        time += PHYLIB_SIM_RATE; 
    }

    newTable->time = time; 
    return newTable;
}

char *phylib_object_string( phylib_object *object ){
    static char string[80];
    if (object==NULL){
        snprintf( string, 80, "NULL;" );
        return string;
    }
    switch (object->type){
        case PHYLIB_STILL_BALL:
            snprintf(string, 80, "STILL_BALL (%d,%6.1lf,%6.1lf)",
                    object->obj.still_ball.number,
                    object->obj.still_ball.pos.x,
                    object->obj.still_ball.pos.y );
            break;
        case PHYLIB_ROLLING_BALL:
            snprintf(string, 80, "ROLLING_BALL (%d,%6.1lf,%6.1lf,%6.1lf,%6.1lf,%6.1lf,%6.1lf)",
                    object->obj.rolling_ball.number,
                    object->obj.rolling_ball.pos.x,
                    object->obj.rolling_ball.pos.y,
                    object->obj.rolling_ball.vel.x,
                    object->obj.rolling_ball.vel.y,
                    object->obj.rolling_ball.acc.x,
                    object->obj.rolling_ball.acc.y );
            break;
        case PHYLIB_HOLE:
            snprintf(string, 80,"HOLE (%6.1lf,%6.1lf)",
                    object->obj.hole.pos.x,
                    object->obj.hole.pos.y );
            break;
        case PHYLIB_HCUSHION:
            snprintf( string, 80, "HCUSHION (%6.1lf)",
                    object->obj.hcushion.y );
            break;
        case PHYLIB_VCUSHION:
            snprintf( string, 80, "VCUSHION (%6.1lf)",
                    object->obj.vcushion.x );
            break;
    }
    return string;
}
